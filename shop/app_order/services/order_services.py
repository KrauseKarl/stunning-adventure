from app_cart.models import Cart
from app_item.models import Item


def get_order():
    pass
def _check_pay_way():
    pass

def _get_item(item):
    return Item.objects.get(id=item.id)


def _get_cart(user):
    return Cart.objects.get(user=user)


def white_off_item_from_store(user):
    cart = _get_cart(user)
    for item in cart.items.all():
        quantity = item.quantity
        item_in_store = _get_item(item)
        if item_in_store.quantity >= quantity:
            item_in_store.quantity -= quantity
            item_in_store.save(update_fields='quantity')
    del cart
    return user

