from django.contrib.auth.models import User
from django.db import models

from app_item.models import Item


class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='cart_item')
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_add_items')
    ordered = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        db_table = 'app_items_in_cart'
        ordering = ['item']
        verbose_name = 'выбранный товар'

    def __str__(self):
        return f'{self.quantity} of {self.item}'

    def total_price(self):
        return self.quantity * self.item.get_price()


class Cart(models.Model):
    items = models.ManyToManyField(CartItem, related_name='all_items')
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_cart')
    ordered = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        db_table = 'app_carts'
        ordering = ['created']
        verbose_name = 'заказ'

    def __str__(self):
        return f'cart {self.pk}'

    def get_total_price(self):
        return float(sum(item.total_price() for item in self.items.all()))

    def get_total_quantity(self):
        return sum(item.quantity for item in self.items.all())


