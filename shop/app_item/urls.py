from django.urls import path
from app_item.views import ItemList, ItemDetail, MainPage, DeleteComment, EditComment

app_name = 'app_item'

urlpatterns = [
    # path('', MainPage.as_view(), name='main_page'),
    path('list/', ItemList.as_view(), name='item_list'),
    path('category/<slug:category>/', ItemList.as_view(), name='item_category'),
    path('color/<slug:color>/', ItemList.as_view(), name='item_color'),
    path('tag/<slug:tag>/', ItemList.as_view(), name='item_tag'),
    path('sorted/<slug:order_by>/', ItemList.as_view(), name='item_sort'),
    path('detail/<int:pk>/', ItemDetail.as_view(), name='item_detail'),
    path('detail/<int:pk>/delete/comment/<int:comment_id>/', DeleteComment.as_view(), name='comment_delete'),
    path('detail/<int:pk>/edit/comment/<int:comment_id>/', EditComment.as_view(), name='comment_edit'),
]
