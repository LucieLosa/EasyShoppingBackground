import csv

from django.contrib import admin
from django.http import HttpResponse

from bazaar.models import Event, EventUser, EventSeller, Item
from django.utils.translation import gettext as _


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["name", "short_name", "date", "is_active", "is_closed"]
    list_filter = ("is_active",)
    search_fields = ("name__startswith",)
    exclude = ("x_user",)


@admin.register(EventUser)
class EventUserAdmin(admin.ModelAdmin):
    list_display = ["event", "user"]
    exclude = ("x_user",)


class ItemInlineAdmin(admin.TabularInline):
    model = Item
    fields = ("cart", "order", "price")

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        return list(super().get_fields(request, obj))

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'event_seller',
            'cart',
            "x_user"
        )


@admin.register(EventSeller)
class EventSellerAdmin(admin.ModelAdmin):
    list_display = [

        "identifier", "seller", 'total_sold_items', "total_sales_amount", "total_fees", "is_no_fees", "event", ]
    list_filter = ("event", "is_no_fees")
    readonly_fields = ['total_sold_items', "total_sales_amount", "total_fees"]
    exclude = ("x_user",)
    inlines = (
        ItemInlineAdmin,
    )
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        # field_names = [field.name for field in meta.fields]
        field_names = [
            "identifier", "seller_name", "total_sales_amount", "fee_value_percentage", "total_payout",
            "total_sold_items"]
        field_names_header = [
            _("Number"), _("Name", "seller"), _("Totally earned"), "10%", _("To payout"), _("Sold items")
        ]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names_header)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = _("Export event sellers")
