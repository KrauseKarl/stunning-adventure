from django.shortcuts import render
from django.views.generic import ListView
from app_item.models import Item, Category


class ItemList(ListView):
    model = Item
    template_name = 'items/item_list.html'
    context_object_name = 'items'
