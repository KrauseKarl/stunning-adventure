from itertools import chain
from django import forms
from django.contrib import admin
from django.contrib.admin.checks import must_be, BaseModelAdminChecks
from django.utils.safestring import mark_safe

from app_item import forms
from app_item.forms import ItemForm
from app_item.models import Item, Category, Tag, Comment
from app_cart.models import Cart, CartItem


class ItemTagsInline(admin.TabularInline):
    model = Item.tag.through
    raw_id_fields = ['tag', ]
    extra = 1


class ItemAdmin(admin.ModelAdmin):
    form = ItemForm
    fields = (
        ('title', 'slug'), ('price', 'stock', 'is_available', 'limited_edition'),
        ('reviews', 'comments'), ('category', 'image'), 'color')
    list_display = ['title', 'full_image', 'category', 'price', 'stock', 'set_colors']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ItemTagsInline, ]
    radio_fields = {'color': admin.VERTICAL}
    list_filter = ('is_available', 'limited_edition', 'category',)
    readonly_fields = ('reviews', 'comments')
    raw_id_fields = ['category', 'tag']

    def full_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width=80/>')

    full_image.short_description = "изображение"
    full_image.allow_tags = True

    def set_colors(self, obj):
        if obj.color:
            return mark_safe(f'<div style="background-color:{obj.color}; box-shadow: 0 0 2px; padding: 20px"></div>')
        return mark_safe(f'<div>не определен </div>')

    set_colors.short_description = "цвет товара"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent_category', 'description']
    prepopulated_fields = {'slug': ('title',)}


class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ItemTagsInline, ]


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'review']


class OrderItemInline(admin.StackedInline):
    model = Cart.items.through
    extra = 1


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['item', 'quantity', 'user', 'ordered']


class CartAdmin(admin.ModelAdmin):
    list_display = ['created', 'user', 'ordered']
    inlines = [OrderItemInline, ]
    fields = [('user', 'ordered'), ]
    readonly_fields = ['user', 'ordered']
    exclude = ['items', ]


admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
