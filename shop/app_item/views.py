from django.contrib.sessions.models import Session
from django.db.models import Q, Min, Max, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.models import User
from django.core.serializers import serialize

from app_item.forms import CommentForm
from app_item.models import Item, Category, Comment, Tag, ItemView
from app_item.services.item_services import AddItemToReview, ItemHandler


class MainPage(TemplateView):
    model = Item
    template_name = 'main-page.html'

    def get_context_data(self, **kwargs):
        favorite = AddItemToReview()
        item_handler = ItemHandler()
        kwargs['favorites'] = favorite.get_favorite_category_items(user=self.request.user)
        kwargs['popular'] = item_handler.get_popular_items
        kwargs['limited_edition_items'] = item_handler.get_limited_edition_items()[:8]
        return kwargs

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class TagMixin(ListView):
    def get_tag_queryset(self, **kwargs):
        try:
            slug = kwargs['slug']
            tag = get_object_or_404(Tag, slug=slug)
            queryset = self.queryset.filter(tag=tag.id)
        except:
            queryset = self.queryset
        return queryset


class FilterMixin(TagMixin, ListView):

    def get_my_queryset(self, queryset, **kwargs):
        try:
            param = kwargs['order_by']
            queryset = queryset.order_by(param)
            return queryset
        except:
            return self.queryset


class ItemList(FilterMixin, TagMixin, ListView):
    model = Item
    template_name = 'app_item/item_list.html'
    context_object_name = 'items'
    queryset = Item.objects.filter(is_available=True).order_by('-reviews')
    extra_context = {'tags': Tag.objects.all()}

    def get(self, request, category=None, tag=None, order_by=None, **kwargs):

        if category:
            category = get_object_or_404(Category, slug=category)
            queryset = self.queryset.filter(category=category.id)
            # try:
            #     queryset = request.session['queryset']
            #     queryset = queryset.filter(category=category.id)
            #     queryset = serialize(queryset=queryset, format='json')
            #     request.session['queryset'] = queryset
            #
            # except:
            #     queryset = self.queryset.filter(category=category.id)
            #     queryset = serialize(queryset=queryset, format='json')
            #     request.session['queryset'] = queryset

        elif tag:

            tag = get_object_or_404(Tag, slug=tag)
            queryset = self.queryset.filter(tag=tag.id)

        else:
            queryset = self.queryset

            # if order_by:
            #     try:
            #         queryset = request.session['queryset']
            #         queryset = queryset.order_by(order_by)
            #         request.session['queryset'] = queryset
            #     except:
            #         queryset = self.queryset.order_by(order_by)
            #         queryset = serialize(queryset=queryset, format='json')
            #         request.session['queryset'] = queryset

        tags = Tag.objects.all()
        # queryset = self.get_my_queryset(self.get_tag_queryset(**kwargs), **kwargs)
        return render(request, 'app_item/item_list.html', context={'items': queryset, 'tags': tags})


class ItemDetail(DetailView, CreateView):
    model = Item
    context_object_name = 'item'
    template_name = 'app_item/item_detail.html'
    form_class = CommentForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        """Добавляет товар к списку просмотренных товаров."""

        add_to_reviews = AddItemToReview()
        add_to_reviews.add_item_to_review(item=self.get_object(), user=request.user)
        # if self.request.user.is_anonymous:
        #     if not User.objects.get(username='Anon'):
        #         user = User.objects.create_user('Anon', 'anon@mail.com', 'Anon@123')
        #         from django.forms.models import model_to_dict
        #         data = model_to_dict(user, fields=('username',))
        #         import json
        #         serialized = json.dumps(data)
        #         print(serialized)
        #         request.session['user'] = serialized
        #     else:
        #         user = User.objects.get(username='Anon')
        #         from django.forms.models import model_to_dict
        #         data = model_to_dict(user, fields=('username',))
        #         data['username'] = 'Oleg'
        #         import json
        #         serialized = json.dumps(data)
        #         print(serialized)
        #         request.session['user'] = serialized
        # else:
        #     try:
        #         del request.session['user']
        #     except KeyError:
        #         pass
        #
        #     # количество просмотров товара
        # item.record_view(self.request, item.id)
        #
        # # создание записи с БД о просмотренном товаре пользователем
        # if user.is_authenticated:
        #     if item not in user.profile.review_items.all():
        #         user.profile.review_items.add(item)
        self.object = self.get_object()
        item = self.get_object()
        user = request.user

        # if user.is_authenticated:
        #     session = request.session.session_key
        form = self.get_form()
        tags = Tag.objects.filter(item_tags=item.id)
        context = {'form': form, 'tags': tags, 'item': item}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return redirect(self.request.get_full_path())

    def form_valid(self, form):
        item = self.get_object()
        form = CommentForm(self.request.POST)
        new_comment = form.save(commit=False)
        new_comment.item = item

        new_comment.save()
        return redirect(self.request.get_full_path())
