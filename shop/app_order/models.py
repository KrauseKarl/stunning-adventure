from django.db import models
from app_cart.models import Cart
from django.contrib.auth.models import User


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'
    STATUS_DEACTIVED = 'deactive'

    STATUS = (
        (STATUS_NEW, 'Новый'),
        (STATUS_IN_PROGRESS, 'В обработке'),
        (STATUS_READY, 'Готов'),
        (STATUS_COMPLETED, 'Выполнен'),
        (STATUS_DEACTIVED, 'Отменен')
    )
    DELIVERY = (
        ('express', 'экспресс'),
        ('standart', 'обычная'),
    )
    PAY_TYPE = (
        ('my_card', 'Онлайн картой'),
        ('some_card', 'Онлайн со случайного чужого счета')
    )
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_order')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_order')

    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    telephone = models.CharField(max_length=10)
    delivery = models.CharField(max_length=12, choices=DELIVERY)
    pay_type = models.CharField(max_length=10, choices=PAY_TYPE)
    city = models.CharField(max_length=10)
    address = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated = models.DateTimeField(auto_now_add=True, verbose_name='дата обновления')
    status = models.CharField(max_length=20, choices=STATUS)
    error = models.CharField(max_length=20, default='')
    objects = models.Manager()

    class Meta:
        db_table = 'app_order'
        ordering = ['created']
        verbose_name = 'заказ'
