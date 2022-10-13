from django.urls import path

from app_order.views import OrderCreate, SuccessOrdered, FailedOrdered, OrderList, OrderDetail

app_name = 'app_order'

urlpatterns = [
    path('create/', OrderCreate.as_view(), name='order_create'),
    path('order_list/', OrderList.as_view(), name='order_list'),
    path('order_detail/<int:pk>/', OrderDetail.as_view(), name='order_detail'),
    path('success_order/', SuccessOrdered.as_view(), name='success_order'),
    path('failed_order/', FailedOrdered.as_view(), name='failed_order'),
]
