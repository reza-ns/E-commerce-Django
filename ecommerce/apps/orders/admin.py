from django.contrib import admin
from . import models


class InvoiceItemInline(admin.TabularInline):
    model = models.InvoiceItem
    extra = 0


class InvoiceAdmin(admin.ModelAdmin):
    inlines = (InvoiceItemInline,)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('refid', 'amount', 'status', 'created_at')


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('zipcode', 'country', 'state', 'user')


admin.site.register(models.Invoice, InvoiceAdmin)
admin.site.register(models.Payment, PaymentAdmin)
admin.site.register(models.Shipping, ShippingAddressAdmin)
