from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('shipping', views.ShippingView.as_view(), name='shipping'),
    path('invoice', views.CheckoutView.as_view(), name='invoice'),
    path('payment', views.PaymentView.as_view(), name='payment'),
    path('verify', views.PaymentVerify.as_view(), name='verify'),
]