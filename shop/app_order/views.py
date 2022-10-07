from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, ListView

from app_cart.models import Cart
from app_order.forms import OrderForm
from app_order.models import Order


class OrderCreate(CreateView):
    model = Order
    template_name = 'app_order/create_order.html'
    form_class = OrderForm

    def form_valid(self, form):
        obj = form.save()
        user = self.request.user
        cart = Cart.objects.filter(user=user).first()
        order, created = Order.objects.create(
            cart=cart,
            user=user,
            email=obj.cleaned_data.get('mail'),
            telephone=obj.cleaned_data.get('phone'),
            delivery=obj.cleaned_data.get('delivery'),
            pay_type=obj.cleaned_data.get('pay'),
            city=obj.cleaned_data.get('city'),
            address=obj.cleaned_data.get('address')
        )
        order.status = 'new'
        order.save()
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
