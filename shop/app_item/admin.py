from django.contrib import admin
from app_item.models import Item, Category, Tag, Comment


class ItemTagsInline(admin.TabularInline):
    model = Item.tag.through


class ItemAdmin(admin.ModelAdmin):
    fields = (
    ('title', 'slug'), ('price', 'stock'), ('is_available', 'limited_edition', 'reviews', 'comments'), 'category')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ItemTagsInline, ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}


class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ItemTagsInline, ]


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'review']


admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
