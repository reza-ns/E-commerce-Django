from django.shortcuts import render
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ShippingForm
from . import models
from apps.shop.models import Product


def _total_price(cart):
    total = 0
    if cart:
        for item in cart:
            total += item['price'] * item['quantity']
    return total


class ShippingView(View):
    def get(self, request):
        shippings = models.Shipping.objects.filter(user=request.user)
        shipping_form = ShippingForm()
        context = {
            'shippings': shippings,
            'shipping_form': shipping_form,
        }
        return render(request, 'orders/shipping.html', context)

    def post(self, request):
        shipping_form = ShippingForm(request.POST)
        if shipping_form.is_valid():
            address = shipping_form.save(commit=False)
            address.user = request.user
            address.save()
        return HttpResponseRedirect(reverse('orders:shipping'))


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        invoice = models.Invoice.objects.filter(user=request.user).last()
        # if invoice.exists():
        return render(request, 'orders/checkout.html', {'invoice': invoice})

    def post(self, request):
        cart = request.session.get('cart', None)
        if not cart:
            invoice = models.Invoice.objects.filter(user=request.user).last()
            if invoice.exists():
                return render(request, 'orders/checkout.html', {'invoice': invoice})

        shipping_id = request.POST.get('shipping_id')
        shipping = models.Shipping.objects.get(id=shipping_id)
        invoice = models.Invoice(
            user=request.user,
            total_price=_total_price(cart),
            shipping=shipping,
        )
        invoice.save()

        product_ids = [item['id'] for item in cart]
        products = Product.objects.filter(pk__in=product_ids)
        invoice_items = []
        for item in cart:
            product = products.get(pk=item['id'])
            invoice_items.append(models.InvoiceItem(
                name=product.name,
                price=product.get_price(),
                count=item['quantity'],
                product=product,
                invoice=invoice
            ))
        models.InvoiceItem.objects.bulk_create(invoice_items)
        request.session['cart'] = []
        return HttpResponseRedirect(reverse('orders:checkout'))