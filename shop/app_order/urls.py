from django.urls import path
from app_cart.views import CartDetail, AddItemCart, RemoveItemCart

app_name = 'app_order'

urlpatterns = [
    # path('add/<int:pk>/', AddItemCart.as_view(), name='add_cart'),
    # path('remove/<int:pk>/', RemoveItemCart.as_view(), name='remove_cart'),
    # path('cart/', CartDetail.as_view(), name='cart'),
]
