from django.contrib.auth.models import User
from django.db.models import Q

from app_cart.models import Cart, CartItem


def _get_user(request):
    return User.objects.get(id=request.user.id)


def get_cart(request):
    try:
        user = _get_user(request)
        cart = Cart.objects.get(user=user)
        cart_total_sum = cart.get_total_price()
        return {'cart_total_sum': cart_total_sum}
    except:
        return {'cart_total_sum': 0}


def get_all_items_in_cart(request):
    try:
        user = _get_user(request)
        all_items = CartItem.objects.filter(Q(user_id=user.id) & Q(is_paid=False)).count()
        return {'all_items': all_items}
    except:
        return {'all_items': None}


def cart(request):
    try:
        cart = Cart.objects.get(user=_get_user(request))
        return {'cart': cart}
    except:
        return {'cart': None}
