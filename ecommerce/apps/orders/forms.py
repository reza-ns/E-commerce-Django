from django.forms import ModelForm
from .models import Shipping


class ShippingForm(ModelForm):
    class Meta:
        model = Shipping
        fields = ('phone', 'address', 'country', 'state', 'zipcode')
