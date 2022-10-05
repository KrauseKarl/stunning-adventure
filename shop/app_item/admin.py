from django.contrib import admin

from app_item.models import Item, Category, Tag, Comment
from app_cart.models import Cart, CartItem


class ItemTagsInline(admin.TabularInline):
    model = Item.tag.through



class ItemAdmin(admin.ModelAdmin):
    fields = (
        ('title', 'slug'), ('price', 'stock', 'is_available', 'limited_edition'),
        ('reviews', 'comments'), ('category', 'image'))
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ItemTagsInline, ]
    list_filter = ('is_available', 'category')
    readonly_fields = ('reviews', 'comments')


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
