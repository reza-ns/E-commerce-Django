from django.db import models
from django.contrib.auth import get_user_model
from apps.shop.models import Product

User = get_user_model()


class Invoice(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_PAID = 'paid'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_PAID, 'Paid'),
    )
    number = models.CharField(max_length=100, null=True, blank=True)
    total_price = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipping = models.ForeignKey('Shipping', on_delete=models.PROTECT,null=True, related_name='invoices')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='invoices')


class InvoiceItem(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    count = models.IntegerField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='invoice_items')
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name='invoice_items')


class Payment(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_SUCCESS = 'success'
    STATUS_FAILED = 'failed'
    STATUS_CANCELED = 'canceled'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_SUCCESS, 'Success'),
        (STATUS_FAILED, 'Failed'),
        (STATUS_CANCELED, 'Canceled')
    )
    amount = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    refid = models.CharField(max_length=100, null=True, blank=True)
    authority = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    invoice = models.ForeignKey('Invoice', on_delete=models.PROTECT, related_name='payments')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payments')


class Shipping(models.Model):
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='shipping_addresses')
