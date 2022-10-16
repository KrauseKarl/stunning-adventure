from django.core.exceptions import ObjectDoesNotExist

from app_cart.models import Cart
from app_cart.services.cart_services import get_active_cart
from app_item.services.item_services import get_item
from app_order.models import Order


def get_order(user):
    """Функция для получения списка всех заказов начиная с последнего"""
    try:
        return Order.objects.filter(user=user).order_by('-created')
    except ObjectDoesNotExist:
        return None


def white_off_item_from_store(user):
    """Функция для списания товара со склада"""
    cart = get_active_cart(user)
    for item in cart.items.all():
        quantity = item.quantity
        item_in_store = get_item(item)
        if item_in_store.quantity >= quantity:
            item_in_store.quantity -= quantity
            item_in_store.save(update_fields='quantity')
    del cart
    return user
