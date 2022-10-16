from app_order.models import Order


def order(request):
    try:
        order = Order.objects.filter(user=request.user, status='new')
        return {'order': order}
    except:
        return {'order': None}