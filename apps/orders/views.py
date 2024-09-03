from django.shortcuts import render, get_object_or_404
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from config import settings
# Third party
from zeep import Client
# Local
from .forms import ShippingForm
from . import models
from apps.shop.models import Product


def _total_price(cart):
    total = 0
    if cart:
        for item in cart:
            total += item['price'] * item['quantity']
    return total


class ShippingView(LoginRequiredMixin, View):
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
        return HttpResponseRedirect(reverse('orders:invoice'))



class PaymentView(LoginRequiredMixin, View):
    def get(self, request):
        invoice = models.Invoice.objects.filter(user=request.user).last()
        payment = models.Payment(
            user =invoice.user, invoice=invoice, amount=invoice.total_price,
            description=f"Payment for invoice #{invoice.pk}",
        )

        callback_url = 'http://' + str(get_current_site(request)) + reverse('orders:verify')
        psp = Client(settings.psp_url)
        MID = settings.MID
        res = psp.service.PaymentRequest(
            MID, payment.amount, payment.description, payment.user.email, '', callback_url
        )
        if res.Status == 100 and len(res.Authority) == 36:
            payment.authority = res.Authority
            payment.save()
            return HttpResponseRedirect(f'https://www.zarinpal.com/pg/StartPay/{payment.authority}')
        else:
            payment.status = models.Payment.STATUS_FAILED
            payment.save()
            return HttpResponseServerError


class PaymentVerify(View):
    def get(self, request):
        authority = request.GET.get('Authority')
        payment = get_object_or_404(models.Payment, authority=authority)
        if request.GET.get('Status') == 'OK':
            psp = Client(settings.psp_url)
            MID = settings.MID
            res = psp.service.PaymentVerification(
                MID, payment.authority, payment.amount
            )

            if res.Status == 100:
                payment.refid = res.RefID
                payment.status = models.Payment.STATUS_SUCCESS
                payment.save()
                payment.invoice.status = models.Invoice.STATUS_PAID
                payment.invoice.number = res.RefID
                payment.invoice.save()
                return render(request, 'orders/payment_success.html', {'payment': payment})
            elif res.Status ==101:
                payment.status = models.Payment.STATUS_SUCCESS
                payment.save()
                return render(request, 'orders/payment_success.html', {'payment': payment})
            elif res.Status == -22:
                payment.status = models.Payment.STATUS_FAILED
                payment.save()
                return render(request, 'orders/payment_failed.html')
            else:
                return render(request, 'orders/payment_failed.html')
        elif request.GET.get('Status') == 'NOK':
            payment.status = models.Payment.STATUS_CANCELED
            payment.save()
            return render(request, 'orders/payment_failed.html')
        else:
            return render(request, 'orders/payment_failed.html')