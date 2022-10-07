from django import forms

from app_order.models import Order


class OrderForm(forms.ModelForm):
    DELIVERY_WAY = (
        ('1', 'Обычная доставка'),
        ('2', 'Экспресс доставка')
    )
    PAY_WAY = (
        ('1', 'Онлайн картой'),
        ('2', 'Онлайн со случайного чужого счета')
    )
    payment = forms.ChoiceField(widget=forms.RadioSelect, choices=PAY_WAY)
    delivery = forms.ChoiceField(widget=forms.RadioSelect, choices=DELIVERY_WAY)

    class Meta:
        model = Order
        fields = '__all__'

