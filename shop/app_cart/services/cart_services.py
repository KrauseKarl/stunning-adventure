from django.contrib.auth.models import User, AnonymousUser
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, redirect

from app_cart.models import CartItem, Cart
from app_item.models import Item
from app_item.services.item_services import get_item


def get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(user=user, ordered=False)
    return cart


def get_active_cart(request, user):
    """Функция возвращает последнюю корзину"""

    if not user.is_anonymous:
        if request.session.get('my_cart', False):
            item_list = request.session['my_cart']
            cart = Cart.objects.filter(user=user, ordered=False).order_by('-created').first()
            for i in item_list:
                item = Item.objects.get(id=i['id'])
                price = float(i['price'])
                cart_item = CartItem.objects.create(item=item, price=price, user=user)

                cart.items.add(cart_item)
                cart.save()
            del request.session['my_cart']
        else:
            cart = Cart.objects.filter(user=user, ordered=False).order_by('-created').first()
        return cart
    else:
        item_list = request.session['my_cart']
        cart = Cart.objects.create(ordered=False)
        for i in item_list:
            item = Item.objects.get(id=i['id'])
            price = float(i['price'])
            cart_item = CartItem.objects.create(item=item, price=price)
            cart.items.add(cart_item)
        return cart



class CartHandler:
    def __init__(self, request, user, **kwargs):
        self.request = request
        self.user = user
        self.item = kwargs['pk']
        self.path = kwargs['path']

    def add_to_cart(self, **kwargs):

        item = get_item(self.item)
        item_for_cart = self._get_or_create_item_for_cart()
        try:
            cart = get_or_create_cart(self.user)
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

    def remove_from_cart(self, **kwargs):
        """Функция для удаления товара из корзины"""
        item = get_item(self.item)
        cart = get_or_create_cart(self.user)
        item_for_cart = get_object_or_404(CartItem, user=self.user, item=item, is_paid=False)

        if item_for_cart in cart.items.all():
            try:
                cart.items.get(id=item_for_cart.id).delete()
            except ObjectDoesNotExist:
                pass
        return redirect(self.path)

    def _get_or_create_item_for_cart(self):
        item = get_item(self.item)
        item_for_cat, created = CartItem.objects.get_or_create(
            user=self.user,
            item=item,
            price=item.price,
            is_paid=False, )
        return item_for_cat

    # def _get_cart_to_add(self):
    #     return Cart.objects.filter(user=self.user, ordered=False)

    # def _get_or_404_order_item(self):
    #     item = self._get_item()
    #     order_item = get_object_or_404(CartItem, user=self.user, item=item, is_paid=False)
    #
    #     return order_item
