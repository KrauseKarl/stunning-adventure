from dataclasses import dataclass, InitVar
from datetime import datetime, timezone

from django.contrib.auth.models import User
from django.core.cache.utils import make_template_fragment_key
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.shortcuts import get_object_or_404, redirect
from django.core.cache import cache
from app_item.models import ItemView, Item


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


