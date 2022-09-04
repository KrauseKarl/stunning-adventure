from django.urls import path
from app_item.views import ItemList, ItemDetail, MainPage

urlpatterns = [
    path('', MainPage.as_view(), name='main_page'),
    path('list/', ItemList.as_view(), name='item_list'),
    path('category/<slug:category>/', ItemList.as_view(), name='item_category'),
    path('tag/<slug:tag>/', ItemList.as_view(), name='item_tag'),
    path('sorted/<slug:order_by>/', ItemList.as_view(), name='item_sort'),
    path('detail/<int:pk>/', ItemDetail.as_view(), name='item_detail'),
]


