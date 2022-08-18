from django.shortcuts import render
from django.views.generic import ListView, DetailView
from app_item.models import Item, Category


class ItemList(ListView):
    model = Item
    template_name = 'items/item_list.html'
    context_object_name = 'items'


class ItemDetail(DetailView):
    model = Item
    context_object_name = 'item'
    template_name = 'items/item_detail.html'

    def get_object(self, *args, **kwargs):
        """ Увеличивает количество просмотров товара при каждом просмотре. """

        obj = super().get_object()
        obj.reviews += 1
        obj.save()
        return obj
