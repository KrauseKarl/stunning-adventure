from django.contrib import admin
from app_item.models import Item, Category


class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'reviews', 'comments', 'is_available', 'category']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']


admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
