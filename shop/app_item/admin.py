from django.contrib import admin
from app_item.models import Item, Category


class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'reviews', 'comments', 'is_available', 'category']
    prepopulated_fields = {'slug': ('title',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
