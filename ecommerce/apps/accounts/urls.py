from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('orders', views.OrdersView.as_view(), name='orders'),
    path('invoice/<str:invoice_number>', views.OrderInvoiceView.as_view(), name='invoice'),
]

