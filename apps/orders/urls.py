from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('shipping', views.ShippingView.as_view(), name='shipping'),
    path('payment', views.CheckoutView.as_view(), name='checkout'),
]