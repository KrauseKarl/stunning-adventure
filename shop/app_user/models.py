from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.core.validators import RegexValidator
from app_item.models import Item


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='profiles')
    avatar = models.ImageField(upload_to='avatar/')
    telephone = models.CharField(max_length=10, validators=[RegexValidator, ])
    date_joined = models.DateTimeField(auto_now_add=True, null=True)  # readonly_fields = ['date_joined',   ]
    review_items = models.ManyToManyField(Item, related_name='items', null=True)

    class Meta:
        ordering = ['user']
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def add(self, obj):
        item = Item.objects.get(obj)
        review_items = self.review_items
        review_items.add(item)
        review_items.save()
        return review_items

