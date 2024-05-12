from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext as _

from bazaar.models import Cart, Item


class ItemInlineAdmin(admin.TabularInline):
    model = Item
    ordering = ("order", "event_seller")
    fields = ("order", "event_seller", "price",)
    extra = 1

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(ItemInlineAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'event_seller':
            if request._obj_ is not None:
                field.queryset = field.queryset.filter(event=request._obj_.event)
            else:
                field.queryset = field.queryset.none()
        return field

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'event_seller',
            'cart',
            "x_user"
        )


class UserFilter(SimpleListFilter):
    title = _("User")
    parameter_name = "user"

    def lookups(self, request, model_admin):
        return [(c.id, f"{c.easho_user.prefix} ({c.username})") for c in
                set([c.user for c in model_admin.model.objects.all()])]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user__id=self.value())


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["identifier", "items_count", "total_price", "is_checked", "x_created", "event", "user"]
    list_filter = ("event", UserFilter, "is_checked",)
    exclude = ("x_user",)
    ordering = ("-x_created",)

    inlines = (
        ItemInlineAdmin,
    )

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        return super(CartAdmin, self).get_form(request, obj, **kwargs)

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
    get_is_checked.short_description = _("Checked")

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
