from datetime import datetime

from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from app_user.models import User, Profile


class ItemView(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='views')
    ip = models.CharField(max_length=40)
    session = models.CharField(max_length=40)
    created = models.DateTimeField(default=datetime.now())


class Item(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name='название')
    slug = models.SlugField(max_length=100, db_index=True, allow_unicode=True)
    description = models.TextField(null=True, blank=True, verbose_name='описание')
    stock = models.PositiveIntegerField(verbose_name='количество')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='цена')
    is_available = models.BooleanField(default=False, verbose_name='в наличии')
    limited_edition = models.BooleanField(default=False, verbose_name='ограниченный тираж')
    reviews = models.SmallIntegerField(default=0, verbose_name='просмотры')
    comments = models.SmallIntegerField(default=0, verbose_name='комментарии')
    created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated = models.DateTimeField(auto_now_add=True, verbose_name='дата обновления')

    image = models.ImageField(upload_to='item/%Y/%m/%d', null=True, blank=True, verbose_name='изображение')

    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, related_name='items',
                                 verbose_name='категория')
    tag = models.ManyToManyField('Tag', max_length=20, blank=True, related_name='items', verbose_name='тег')

    class Meta:
        ordering = ['created']
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Функция по созданию slug"""
        if not self.slug:
            self.slug = slugify(self.title)
        super(Item, self).save(*args, **kwargs)

    def record_view(self, request, item_id):
        """Функция увеличивает  количество просмотров при посещении страницы товара"""
        item = get_object_or_404(Item, pk=item_id)
        if request.user.is_authenticated:
            if not ItemView.objects.filter(
                    item=item,
                    session=request.session.session_key):
                view = ItemView.objects.create(
                    item=item,
                    ip=request.META['REMOTE_ADDR'],
                    created=datetime.now(),
                    session=request.session.session_key
                )
                view.save()
        else:
            if not ItemView.objects.filter(
                    item=item,
                    ip=request.META['REMOTE_ADDR']):
                view = ItemView.objects.create(
                    item=item,
                    ip=request.META['REMOTE_ADDR'],
                    created=datetime.now(),
                    session=''
                )
                view.save()
        return ItemView.objects.filter(item=item).count()


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
    title = models.CharField(max_length=50, unique=True, blank=True, verbose_name='название тега')
    slug = models.SlugField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True, verbose_name='активный')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'app_tag'
        verbose_name = 'тег'
        verbose_name_plural = 'теги'


class Comment(models.Model):
    comment_text = models.TextField(verbose_name='комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='дата обновления')
    is_published = models.BooleanField(default=False, verbose_name='опубликовано')
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='comments', verbose_name='товар')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='comments', verbose_name='пользователь')

    def __str__(self):
        return self.comment_text[:15]

    class Meta:
        db_table = 'app_item_comments'
        ordering = ['-created_at']
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'


class Image(models.Model):
    title = models.CharField(max_length=200, null=True, verbose_name='название')
    created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated = models.DateTimeField(auto_now_add=True, verbose_name='дата изменения')
    main_image = models.BooleanField(default=False, verbose_name='главное изображения')
    image = models.ImageField(upload_to='gallery/%Y/%m/%d', default='static/img/default_flat.jpg', null=True,
                              blank=True, verbose_name='изображение')

    class Meta:
        ordering = ['title']
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'

    def __str__(self):
        return self.title
