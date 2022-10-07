from django.contrib import messages

from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from app_cart.models import Cart, CartItem
from app_cart.services.cart_services import CartHandler, get_cart


class AddItemToCart(TemplateView):
    model = Cart
    template_name = 'app_item/item_detail.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        kwargs['path'] = request.META.get('HTTP_REFERER')
        cart = CartHandler(user, **kwargs)
        cart._get_cart()
        order = cart.add_to_cart(user=user, **kwargs)
        messages.info(self.request, "Товар добавлен в корзину")
        return order


class RemoveItemFromCart(TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user
        kwargs['path'] = request.META.get('HTTP_REFERER')
        cart = CartHandler(user, **kwargs)
        order = cart.remove_from_cart(user=user, **kwargs)
        return order


class CartDetail(ListView):
    model = Cart
    template_name = 'app_cart/cart.html'
    context_object_name = 'cart'

    def get_queryset(self):
        user = self.request.user
        queryset = get_cart(user)
        return queryset

