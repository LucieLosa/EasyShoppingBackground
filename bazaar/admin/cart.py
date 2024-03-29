from django.contrib import admin
from django.utils.translation import gettext as _

from bazaar.models import Cart, Item


class ItemInlineAdmin(admin.TabularInline):
    model = Item
    fields = ("event_seller","price",)

    # def user_identifier(self, obj):
    #     return obj.event_seller.identifier

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'event_seller',
            'cart',
            "x_user"
        )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["identifier", "items_count", "total_price", "is_checked", "x_created", "event"]
    list_filter = ("event", "is_checked",)
    exclude = ("x_user",)
    ordering = ("-x_created",)

    inlines = (
        ItemInlineAdmin,
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            "event",
            "user"
        )


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["get_seller", "price", "cart", "get_event", "get_is_checked", "x_created"]
    exclude = ("x_user",)
    list_filter = ("event_seller__event", "cart__is_checked", "cart")

    def get_event(self, obj):
        return obj.event_seller.event

    def get_is_checked(self, obj):
        return obj.cart.is_checked

    get_event.admin_order_field = 'event_seller__event'  # Allows column order sorting
    get_event.short_description = _('Event')

    def get_seller(self, obj):
        return obj.event_seller.identifier

    get_seller.admin_order_field = 'event_seller__seller'  # Allows column order sorting
    get_seller.short_description = _('Seller')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'event_seller',
            'cart',
        )
