# from django.db import models
#
#
# class Order(models.Model):
#     STATUS_NEW = 'new'
#     STATUS_IN_PROGRESS = 'in_progress'
#     STATUS_READY = 'is_ready'
#     STATUS_COMPLETED = 'completed'
#     STATUS_DEACTIVED = 'deactive'
#
#     DELIVERY = (
#         (STATUS_NEW, 'Новый заказ'),
#         (STATUS_IN_PROGRESS, 'Заказ в обработке'),
#         (STATUS_READY, 'Заказ готов'),
#         (STATUS_COMPLETED, 'Заказ выполнен'),
#         (STATUS_DEACTIVED, 'Заказ Отменен')
#     )
#
#     PAY_TYPE = (
#         ('my_card', 'Онлайн картой'),
#         ('some_card', 'Онлайн со случайного чужого счета')
#     )
#     cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=250)
#     middle_name = models.CharField(max_length=250)
#     last_name = models.CharField(max_length=250)
#     email = models.EmailField(max_length=250)
#     telephone = models.CharField(max_length=10)
#     delivery = models.CharField(max_length=12, choices=DELIVERY)
#     pay_type = models.CharField(max_length=10, choices=PAY_TYPE)
#     city = models.CharField(max_length=10)
#     address = models.CharField(max_length=10)
