from dataclasses import dataclass, InitVar
from datetime import datetime, timezone
from typing import List, Dict, Union
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.core.cache.utils import make_template_fragment_key
from django.db.models import Count, Max, Sum, Min
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.shortcuts import get_object_or_404, redirect
from django.core.cache import cache
from app_item.models import ItemView, Item, Category


def get_ip(request):
    ip_address = request.headers.get('X-Forwarded-For', request.META.get('REMOTE_ADDR', '127.0.0.1'))
    return ip_address


def get_session_key(request):
    session_key = request.META.get('session_key', None)
    return session_key


class CountView:

    @staticmethod
    def _get_item(item):
        return get_object_or_404(Item, pk=item)

    def _get_item_view(self, session, item):
        return ItemView.objects.filter(item=item, session=session)

    # def record_view(self, user, item, session, ):
    #     """Функция увеличивает  количество просмотров при посещении страницы товара"""
    #
    #     item = self._get_item(item)
    #     session_key = get_session_key(request)
    #     if user.is_authenticated:
    #         if not ItemView.objects.filter(item=item, session=session):
    #             view = ItemView.objects.create(item=item,
    #                                            ip=request.META['REMOTE_ADDR'],
    #                                            created=datetime.now(),
    #                                            session=request.session.session_key
    #                                            )
    #             view.save()
    #     else:
    #         if not ItemView.objects.filter(item=item, ip=request.META['REMOTE_ADDR']):
    #             view = ItemView.objects.create(item=item,
    #                                            ip=request.META['REMOTE_ADDR'],
    #                                            created=datetime.now(),
    #                                            session=''
    #                                            )
    #             view.save()
    #     return ItemView.objects.filter(item=item).count()


class ItemHandler:
    def get_popular_items(self):
        """Функция возвращает список экземпляров популярных товаров"""
        return Item.available_items.order_by('-reviews')[:8]

    def get_limited_edition_items(self):
        """Функция возвращает список экземпляров товаров «Ограниченный тираж»"""
        return Item.available_items.filter(limited_edition=True)


class AddItemToReview:

    def _get_all_category(self, category_id=None):
        """Функция возвращает одну категорию по ID или при отсутствии ID все категории товаров """
        if category_id:
            return Category.objects.get(id=category_id)
        return Category.objects.all()

    def _get_item(self, item):
        """Функция возвращает экземпляр  товара"""
        item = get_object_or_404(Item, pk=item.pk)
        return item

    def _get_reviews_items(self, user) -> QuerySet[ItemView]:
        """Функция возвращает все товары, которые просматривал пользователь """
        if user.is_authenticated:
            return user.profile.review_items.all()
        return Item.objects.order_by('reviews')

    def _get_favorite_category_list(self, all_reviewed_item: QuerySet[ItemView]):
        """Функция возвращает список самых просматриваемых категорий товаров"""
        return all_reviewed_item.values_list('category').annotate(rating=Count('category')). \
            order_by('-rating')

    def _get_favorite_category_and_price_dict(
            self,
            favorite_category_list: List[str],
            category_list: QuerySet[Category]) -> List[Dict[str, Union[str, float]]]:
        """Функция возвращает список словарей(категория, цена) """

        favorite_category = []
        for item in favorite_category_list:
            favorite_category.append({
                'category': category_list.get(id=item[0]),
                'price': self._get_minimum_price(item[0])
            })
        return favorite_category

    def get_favorite_category_best_price(self, user):
        """Функция возвращает самые популярные категории товаров у пользователя"""

        all_reviewed_item = self._get_reviews_items(user)
        favorite_category_list = self._get_favorite_category_list(all_reviewed_item)
        all_category_list = self._get_all_category()
        favorite_category_best_price = self._get_favorite_category_and_price_dict(
            favorite_category_list, all_category_list
        )

        return favorite_category_best_price

    def _get_minimum_price(self, category_id):
        """Функция возвращает самую низкую цену на товар в категории"""
        cat = self._get_all_category(category_id)
        min_price = cat.items.aggregate(min_price=Min('price'))
        return float(min_price.get('min_price'))

    def add_item_to_review(self, user, item):
        """Функция добавляет товар в список просмотренных"""
        item = self._get_item(item)
        reviews = self._get_reviews_items(user)
        if item not in reviews:
            try:
                user.profile.review_items.add(item)
            except:
                pass
        self.get_favorite_category_best_price(user)
        return reviews

# from django.db import models
#
# class Ip(models.Model): # наша таблица где будут айпи адреса
#     ip = models.CharField(max_length=100)
#
# def __str__(self):
#     return self.ip
#
# class Post(models.Model): # модель у которой будем считать просмотры
#     ...
#     views = models.ManyToManyField(Ip, related_name="post_views", blank=True)
#
#
# # Главная страница тут рендерим все посты
# def home_view(request):
#     posts = Post.objects.all()
#
#     context = {
#         'posts': posts,
#     }
#     return render(request, 'main/home.html', context)
#
# from django.shortcuts import render
# from videos.models import Post, Ip
#
# # Метод для получения айпи
# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR') # В REMOTE_ADDR значение айпи пользователя
#     return ip
# # Страница самого поста
# def post_view(request, slug):
#     post = Post.objects.get(slug=slug)
#
#     ip = get_client_ip(request)
#
#     if Ip.objects.filter(ip=ip).exists():
#         post.views.add(Ip.objects.get(ip=ip))
#     else:
#         Ip.objects.create(ip=ip)
#         post.views.add(Ip.objects.get(ip=ip))
#
#     context = {
#         'post': post,
#     }
#     return render(request, 'main/post.html', context)
