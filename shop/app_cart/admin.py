from django.contrib import admin

from app_cart.models import Cart, CartItem


class OrderItemInline(admin.StackedInline):
    model = Cart.items.through
    extra = 1


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['item', 'quantity', 'user', 'is_paid']
    list_filter = ('user', 'is_paid',)


class CartAdmin(admin.ModelAdmin):
    list_display = ['created', 'user', 'ordered']
    inlines = [OrderItemInline, ]
    fields = [('user', 'ordered'), ]
    readonly_fields = ['user', 'ordered']
    exclude = ['items', ]


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
