from django.contrib import admin

from app_order.models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'created', 'status',
                    'telephone', 'delivery', 'pay',
                    'city', 'address']
    list_filter = ('status',)


admin.site.register(Order, OrderAdmin)
