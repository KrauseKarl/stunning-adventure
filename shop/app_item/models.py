from django.db import models


class Item(models.Model):
    title = models.CharField(max_length=100, verbose_name='название')
    description = models.TextField(null=True, blank=True, verbose_name='описание')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='цена')
    created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated = models.DateTimeField(auto_now_add=True, verbose_name='дата обновления')
    image = models.ImageField(upload_to='item/%Y/%m/%d', null=True, blank=True, verbose_name='изображение')
    reviews = models.SmallIntegerField(default=0, verbose_name='просмотры')
    comments = models.SmallIntegerField(default=0, verbose_name='комментарии')
    is_available = models.BooleanField(default=False, verbose_name='в наличии')
    limited_edition = models.BooleanField(default=False, verbose_name='ограниченный тираж')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True,
                                 related_name='items', verbose_name='категория')

    class Meta:
        ordering = ['created']
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='название')
    description = models.TextField(null=True, blank=True, verbose_name='описание')
    image = models.ImageField(upload_to='category', null=True, verbose_name='иконка')

    class Meta:
        ordering = ['title']
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.title
