from django.contrib import admin
from . import models


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('zipcode', 'country', 'state', 'user')


admin.site.register(models.Shipping, ShippingAddressAdmin)
