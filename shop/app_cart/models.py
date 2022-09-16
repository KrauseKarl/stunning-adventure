from django.contrib.auth.models import User
from django.db import models

from app_item.models import Item


class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
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


class Cart(models.Model):
    items = models.ManyToManyField(CartItem, related_name='orders')
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_orders')
    ordered = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        db_table = 'app_carts'
        ordering = ['created']
        verbose_name = 'заказ'

    def __str__(self):
        return f'{self.user}'

    def get_total_price(self):
        pass
        # return sum()
