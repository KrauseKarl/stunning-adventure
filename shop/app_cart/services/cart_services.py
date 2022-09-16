from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, redirect

from app_cart.models import CartItem, Cart
from app_item.models import Item


class CartHandler:

    @staticmethod
    def _get_item(item):
        return get_object_or_404(Item, pk=item)

    @staticmethod
    def _get_or_create_order_item(user, item):
        order_item, created = CartItem.objects.get_or_create(user=user, item=item, ordered=False)
        return order_item

    @staticmethod
    def _get_order_queryset(user):
        return Cart.objects.filter(user=user, ordered=False)

    def add_to_cart(self, user, **kwargs):
        item = self._get_item(kwargs['pk'])
        order_item = self._get_or_create_order_item(user=user, item=item)
        order_qs = self._get_order_queryset(user)

        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__pk=item.pk).exists():
                order_item.quantity += 1
                order_item.save()
            else:
                order.items.add(order_item)
                order.save()
        else:
            order = Cart.objects.create(user=user)
            order.items.add(order_item)
            order.save()

        @receiver(post_save, sender=CartItem)
        def _update_cache_cart(**kwargs):
            key = make_template_fragment_key('order_story', [user.username])
            cache.delete(key)

        return redirect("app_item:item_detail", pk=item.pk)

    def remove_from_cart(self, user, **kwargs):
        pass
