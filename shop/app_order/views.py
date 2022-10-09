from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import PermissionsMixin
from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, ListView, DetailView

from app_cart.models import Cart
from app_order.forms import OrderForm
from app_order.models import Order


class OrderCreate(CreateView):
    model = Order
    template_name = 'app_order/create_order.html'
    form_class = OrderForm

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        telephone = form.cleaned_data.get('telephone')
        delivery = form.cleaned_data.get('delivery')
        pay = form.cleaned_data.get('pay')
        city = form.cleaned_data.get('city')
        address = form.cleaned_data.get('address')
        total_sum = form.cleaned_data.get('total_sum')
        user = self.request.user
        cart = Cart.objects.filter(user=user, ordered=False).order_by('-created').first()
        Order.objects.create(
            cart=cart,
            user=user,
            name=name,
            email=email,
            telephone=telephone,
            delivery=delivery,
            pay=pay,
            city=city,
            address=address,
            status='new',
            total_sum=total_sum,
        )

        items = cart.items.all()
        for item in items:
            item.ordered = True
            item.save()

        cart.delete()

        return render(self.request, 'app_order/successful_order.html')

    def form_invalid(self, form):
        return render(self.request, 'app_order/failed_order.html')


class SuccessOrdered(TemplateView):
    template_name = 'app_order/successful_order'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class FailedOrdered(TemplateView):
    template_name = 'app_order/failed_order'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class OrderList(ListView):
    model = Order
    template_name = 'app_order/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            queryset = Order.objects.filter(user=user)
            return queryset
        return False


class OrderDetail(DetailView):  #   UserPassesTestMixin PermissionsMixin
    model = Order
    template_name = 'app_order/order_detail.html'
    context_object_name = 'order'

    # def test_func(self):
    #     user = self.request.user
    #     order = self.get_object()
    #     print(order)
    #     if user == order.user:
    #         return True
    #     return False
