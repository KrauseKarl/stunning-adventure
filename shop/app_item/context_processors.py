from django.db.models import Q

from app_item.models import Category


def categories(request):
    return {'categories': Category.available.exclude(Q(items=None) & Q(sub_categories=None))}
