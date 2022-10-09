from django import forms

from app_order.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('email', 'telephone', 'delivery', 'pay', 'city', 'address', 'name', 'total_sum')
