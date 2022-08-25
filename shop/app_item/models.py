from django.db import models
from django.utils.text import slugify


class Item(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name='название')
    slug = models.SlugField(max_length=100, db_index=True, allow_unicode=True)
    description = models.TextField(null=True, blank=True, verbose_name='описание')
    stock = models.PositiveIntegerField(verbose_name='количество')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='цена')
    image = models.ImageField(upload_to='item/%Y/%m/%d', null=True, blank=True, verbose_name='изображение')
    is_available = models.BooleanField(default=False, verbose_name='в наличии')
    limited_edition = models.BooleanField(default=False, verbose_name='ограниченный тираж')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True,
                                 related_name='items', verbose_name='категория')
    reviews = models.SmallIntegerField(default=0, verbose_name='просмотры')
    comments = models.SmallIntegerField(default=0, verbose_name='комментарии')
    created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated = models.DateTimeField(auto_now_add=True, verbose_name='дата обновления')

    class Meta:
        ordering = ['created']
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Item, self).save(*args, **kwargs)


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='название')
    slug = models.SlugField(max_length=100, db_index=True, allow_unicode=True)
    description = models.TextField(null=True, blank=True, verbose_name='описание')
    image = models.ImageField(upload_to='category', null=True, verbose_name='иконка')
    parent_category = models.ForeignKey('self', related_name='sub_categories',
                                        on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)


class Tag(models.Model):
    pass