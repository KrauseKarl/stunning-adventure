from django.urls import path
from app_item.views import ItemList, ItemDetail

urlpatterns = [
    path('', ItemList.as_view(), name='item_list'),
    path('item/<int:pk>/', ItemDetail.as_view(), name='item_detail'),
]
