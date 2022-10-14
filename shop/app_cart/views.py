from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http.response import HttpResponseBase

from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from app_cart.models import Cart, CartItem
from app_cart.services.cart_services import *
from app_item.services.item_services import get_item
from app_user.models import Profile


def get_user(request):
    user = request.user

    if user.is_anonymous:
        return user
    else:
        return User.objects.get(username=user.username)



def SetCookie(request):
    response = HttpResponse()
    response.set_cookie(key='an_cart', value='3333333333333330000', max_age=600)
    return response


class AddItemToCart(TemplateView):
    model = Cart
    template_name = 'app_item/item_detail.html'

    # {'headers': {'Content-Type': 'text/html; charset=utf-8'},
    #  '_charset': None,
    #  '_resource_closers': [],
    #  '_handler_class': None,
    #  'cookies': "< SimpleCookie: cart = '3333333333333330000'" >,
    #  'closed': False,
    #  '_reason_phrase': None
    #  }

    def get(self, request, *args, **kwargs):
        user = get_user(request)
        item = get_item(kwargs['pk'])

        if request.user.is_authenticated:
            kwargs['path'] = request.META.get('HTTP_REFERER')
            cart = CartHandler(request, user, **kwargs)
            cart.add_to_cart(**kwargs)
            path = request.META.get('HTTP_REFERER')
        else:
            if not request.session.get('my_cart'):
                request.session['my_cart'] = []
            request.session['my_cart'].append({'name': item.title, 'id': item.id, 'price': str(item.price)})
            path = request.META.get('HTTP_REFERER')
        return redirect(path)


class RemoveItemFromCart(TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user
        kwargs['path'] = request.META.get('HTTP_REFERER')
        cart = CartHandler(request, user, **kwargs)
        order = cart.remove_from_cart(**kwargs)
        return order


class CartDetail(ListView):
    model = Cart
    template_name = 'app_cart/cart.html'
    context_object_name = 'cart'

    def get_queryset(self):
        user = get_user(self.request)
        queryset = get_active_cart(self.request, user)
        return queryset
