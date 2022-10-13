from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, ListView, DetailView

from app_cart.models import Cart, CartItem
from app_item.models import Item
from app_order.forms import OrderForm
from app_order.models import Order


class OrderCreate(CreateView):
    model = Order
    template_name = 'app_order/create_order.html'
    form_class = OrderForm

    def form_valid(self, form):
        # 1 user
        user = self.request.user
        # 2 cart(user)  # TODO service def _get_user_cart()
        cart = Cart.objects.filter(user=user, ordered=False).order_by('-created').first()
        # 3 create order (user, cart, form) # TODO service def _create_order(user, cart, form)
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        telephone = form.cleaned_data.get('telephone')
        delivery = form.cleaned_data.get('delivery')
        pay = form.cleaned_data.get('pay')
        city = form.cleaned_data.get('city')
        address = form.cleaned_data.get('address')
        total_sum = form.cleaned_data.get('total_sum')
        order = Order.objects.create(
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
        # 4  # TODO service def _set_item_is_paid()
        items = cart.items.all()  # TODO service def _get_all_items_of_cart()
        for item_is_paid in items:
            item_is_paid.is_paid = True  # TODO service def _set_item_is_paid()
            item_is_paid.order = order
            item_is_paid.save()
            item = Item.objects.get(id=item_is_paid.item.id)  # TODO service def _get_item()

            item.stock -= item_is_paid.quantity  # TODO service def _write_off_item_from_store()
            item.save()
        # 5 TODO service def delete_cart()
        cart.delete()  # TODO service def _delete_cart()

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


class OrderList(PermissionRequiredMixin, ListView):
    model = Order
    template_name = 'app_order/order_list.html'
    context_object_name = 'orders'
    permission_required = ('app_order.view_order', 'app_order.change_order')

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            queryset = Order.objects.filter(user=user).order_by('-created')  # TODO service def _get_order()
            return queryset
        return False


class OrderDetail(UserPassesTestMixin, DetailView):  # UserPassesTestMixin PermissionsMixin
    model = Order
    template_name = 'app_order/order_detail.html'
    context_object_name = 'order'

    def test_func(self):
        user = self.request.user
        order = self.get_object()
        if user == order.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items_is_paid'] = CartItem.objects.filter(order=self.get_object()) # TODO service def _get_has_paid_items
        return context
