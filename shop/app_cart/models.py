from django.db import models
from django.contrib.auth.models import User
from app_item.models import Item
from app_order.models import Order


class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='cart_item')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_add_items',
                             verbose_name='покупатель', null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True,
                              related_name='items_is_paid', verbose_name='заказ')

    quantity = models.PositiveIntegerField(default=1,  verbose_name='количество товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена товара')
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая сумма')

    is_paid = models.BooleanField(default=False, verbose_name='статус оплаты')

    objects = models.Manager()

    class Meta:
        db_table = 'app_items_in_cart'
        ordering = ['item']
        verbose_name = 'выбранный товар'

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.item.get_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.quantity}шт. {self.item} в корзине'

    def total_price(self):
        return self.quantity * self.item.get_price()


class Cart(models.Model):
    items = models.ManyToManyField(CartItem, related_name='all_items', verbose_name='товар')
    created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_cart', verbose_name='покупатель')
    ordered = models.BooleanField(default=False, verbose_name='оплаченный')

    objects = models.Manager()

    class Meta:
        db_table = 'app_carts'
        ordering = ['created']
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'

    def __str__(self):
        return f'корзина №00-{self.pk}'

    def get_total_price(self):
        return float(sum(item.total_price() for item in self.items.all()))

    def get_total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    def get_total_q(self):
        return self.items.filter(is_paid=False)

