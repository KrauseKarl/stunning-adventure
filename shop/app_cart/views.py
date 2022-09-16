from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from app_cart.models import Cart, CartItem
from app_cart.services.cart_services import CartHandler


class AddItemCart(TemplateView):
    model = Cart
    template_name = 'app_item/item_detail.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        cart = CartHandler()
        order = cart.add_to_cart(user=user, **kwargs)
        return order


class RemoveItemCart(TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user
        cart = CartHandler()
        order = cart.remove_from_cart(user=user, **kwargs)
        return order


class CartDetail(ListView):
    model = CartItem
    template_name = 'app_cart/cart.html'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = CartItem.objects.filter(user=self.request.user)
        return queryset
