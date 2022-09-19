from django.urls import path
from app_cart.views import CartDetail, AddItemToCart, RemoveItemFromCart

app_name = 'app_cart'

urlpatterns = [
    path('add/<int:pk>/', AddItemToCart.as_view(), name='add_cart'),
    path('remove/<int:pk>/', RemoveItemFromCart.as_view(), name='remove_cart'),
    path('cart/', CartDetail.as_view(), name='cart'),
]
