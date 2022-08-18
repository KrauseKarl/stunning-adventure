from django.urls import path
from app_item.views import ItemList

urlpatterns = [
    path('', ItemList.as_view(), name='item_list'),
]
