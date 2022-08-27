from django.shortcuts import render
from django.views.generic import ListView, DetailView
from app_item.models import Item, Category
from django.contrib.auth.models import AnonymousUser


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

    def get(self, request, *args, **kwargs):

        """Добавляет товар к списку просмотренных товаров."""
        item = self.get_object()
        user = request.user

        # количество просмотров товара
        item.record_view(self.request, item.id)

        # создание записи с БД о просмотренном товаре пользователем
        if user.is_authenticated:
            if item not in user.profile.review_items.all():
                user.profile.review_items.add(item)

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, pk, **kwargs):
        news = News.objects.get(id=pk)
        comments = news.comments.all()
        comment_form = CommentForm(request.POST)
        new_comment = None
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.save()
        else:
            comment_form = CommentForm()
        return render(request, 'app_news/news_detail.html',
                      context={'news': news, 'comments': comments,
                               'new_comment': new_comment, 'comment_form': comment_form})
