from app_cart.models import Cart


def get_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_total_sum = cart.get_total_price()
        return {'cart_total_sum': cart_total_sum}
    except:
        return {'cart_total_sum': 0}

def cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        return {'cart': cart}
    except:
        return {'cart': None}