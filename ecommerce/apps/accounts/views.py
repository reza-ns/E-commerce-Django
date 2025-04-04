from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.orders.models import Payment, Invoice


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'accounts/dashboard_profile.html')


class OrdersView(LoginRequiredMixin, ListView):
    context_object_name = 'orders'
    template_name = 'accounts/dashboard_orders.html'

    def get_queryset(self):
        queryset = Payment.objects.filter(user=self.request.user, status=Payment.STATUS_SUCCESS)
        return queryset


class OrderInvoiceView(LoginRequiredMixin, DetailView):
    context_object_name = 'invoice'
    template_name = 'accounts/dashboard_invoice.html'
    slug_field = 'number'
    slug_url_kwarg = 'invoice_number'

    def get_queryset(self):
        queryset = Invoice.objects.filter(user=self.request.user)
        return queryset




