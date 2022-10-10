from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, redirect

from app_cart.models import CartItem, Cart
from app_item.models import Item


def get_cart(user):
    cart, created = Cart.objects.get_or_create(user=user, ordered=False)
    return cart


class CartHandler:
    def __init__(self, user, **kwargs):
        self.user = user
        self.item = kwargs['pk']
        self.path = kwargs['path']
        self.queryset = self._get_cart()

    def add_to_cart(self, **kwargs):

        item = self._get_item()
        item_for_cart = self._get_or_create_item_for_cart()
        try:
            cart = self._get_cart()
            if cart.items.filter(item__pk=item.pk).exists():
                item_for_cart.quantity += 1
                item_for_cart.save()
            else:
                cart.items.add(item_for_cart)
                cart.save()
        except ObjectDoesNotExist:
            cart = Cart.objects.create(user=self.user)
            cart.items.add(item_for_cart)
            cart.save()

        @receiver(post_save, sender=CartItem)
        def _update_cache_cart(**kwargs):
            key = make_template_fragment_key('order_story', [self.user.username])
            cache.delete(key)

        return redirect(self.path)

    def remove_from_cart(self, user, **kwargs):
        item = self._get_item()
        cart = self._get_cart()
        item_for_cart = get_object_or_404(CartItem, user=user, item=item, is_paid=False)

        if item_for_cart in cart.items.all():
            try:
                cart.items.get(id=item_for_cart.id).delete()
            except ObjectDoesNotExist:
                pass
        return redirect(self.path)

    def _get_item(self):
        return get_object_or_404(Item, pk=self.item)

    def _get_cart(self):
        cart, created = Cart.objects.get_or_create(user=self.user, ordered=False)
        return cart

    def _get_or_create_item_for_cart(self):
        item = self._get_item()
        item_for_cat, created = CartItem.objects.get_or_create(
            user=self.user,
            item=item,
            price=item.price,
            is_paid=False)
        return item_for_cat

    # def _get_cart_to_add(self):
    #     return Cart.objects.filter(user=self.user, ordered=False)

    # def _get_or_404_order_item(self):
    #     item = self._get_item()
    #     order_item = get_object_or_404(CartItem, user=self.user, item=item, is_paid=False)
    #
    #     return order_item


