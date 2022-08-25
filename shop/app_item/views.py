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
        print(obj)
        return obj

    def get(self, request, *args, **kwargs):

        """Добавляет товар к списку просмотренных товаров."""
        self.object = self.get_object()
        user = request.user.profile
        if self.object not in user.review_items.all():
            user.review_items.add(self.object)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
