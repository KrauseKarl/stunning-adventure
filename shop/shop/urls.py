from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from app_item.views import MainPage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPage.as_view(), name='main_page'),
    path('accounts/', include(('app_user.urls', 'app_user'), namespace='app_user')),
    path('item/', include(('app_item.urls', 'app_item'), namespace='app_item')),
    path('cart/', include(('app_cart.urls', 'app_cart'), namespace='app_cart')),
    path('order/', include(('app_order.urls', 'app_order'), namespace='app_order')),
    path('__debug__/', include('debug_toolbar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
