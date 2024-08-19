from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import View
from .forms import CartAddForm
from apps.shop.models import Product


def _add_item_to_cart(cart, cart_item):
    if cart is not None:
        found_item = None
        for item in cart:
            if item['id'] == cart_item['id']:
                found_item = item
                break
        if found_item:
            found_item['quantity'] += cart_item['quantity']
        else:
            cart.append(cart_item)
    elif cart is None:
        cart = [cart_item]
    return cart


def _total_price(cart):
    total = 0
    if cart:
        for item in cart:
            total += item['price'] * item['quantity']
    return total


class CartView(View):
    action = None

    def get(self, request):
        cart = request.session.get('cart', None)
        total = _total_price(cart)
        context = {
            'cart': cart,
            'total_price': total
        }
        return render(request, 'cart/cart.html', context)

    def post(self, request, product_id):
        cart = request.session.get('cart', None)

        if self.action == 'add':
            form = CartAddForm(request.POST)
            if form.is_valid():
                quantity = form.cleaned_data.get('quantity')
                product = get_object_or_404(Product, pk=product_id)
                item = {
                     'id': product.id,
                     'name': product.name,
                     'quantity': quantity,
                     'price': product.get_price()
                     }
                cart = _add_item_to_cart(cart, item)
                request.session['cart'] = cart
                return HttpResponseRedirect(reverse_lazy('shop:product_page', args=[product.slug]))
        elif self.action == 'remove':
            for item in cart:
                if item['id'] == product_id:
                    cart.remove(item)
            request.session['cart'] = cart
            return HttpResponseRedirect(reverse_lazy('cart:cart'))
        else:
            return HttpResponseBadRequest





