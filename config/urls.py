from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.shop.urls', namespace='shop')),
    path('cart/', include('apps.cart.urls', namespace='cart')),
    path('checkout/', include('apps.orders.urls', namespace='orders')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
