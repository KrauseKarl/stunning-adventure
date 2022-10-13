from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    STATUS = (
        ('new', 'Новый'),
        ('in_progress', 'В обработке'),
        ('is_ready', 'Готов'),
        ('completed', 'Выполнен'),
        ('deactivated', 'Отменен')
    )
    DELIVERY = (
        ('express', 'экспресс'),
        ('standard', 'обычная'),
    )
    PAY_TYPE = (
        ('online', 'Онлайн картой'),
        ('someone', 'Онлайн со случайного чужого счета')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_order')

    name = models.CharField(max_length=250, verbose_name='имя получателя')
    status = models.CharField(max_length=20, choices=STATUS,  verbose_name='статус заказа')
    total_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='сумма заказа')
    delivery = models.CharField(max_length=20, choices=DELIVERY, verbose_name='доставка')
    pay = models.CharField(max_length=20, choices=PAY_TYPE, verbose_name='оплата')
    email = models.EmailField(max_length=250, verbose_name='электронная почта')
    telephone = models.CharField(max_length=20, verbose_name='телефон')
    city = models.CharField(max_length=200, verbose_name='город')
    address = models.CharField(max_length=200, verbose_name='адрес')
    created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated = models.DateTimeField(auto_now_add=True, verbose_name='дата обновления')

    error = models.CharField(max_length=200, default='', blank=True)

    objects = models.Manager()

    class Meta:
        db_table = 'app_order'
        ordering = ['created']
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
