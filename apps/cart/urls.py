from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/<int:product_id>', views.CartView.as_view(action='add'), name='cart_add'),
    path('remove/<int:product_id>', views.CartView.as_view(action='remove'), name='cart_remove'),
    path('', views.CartView.as_view(), name='cart'),
]