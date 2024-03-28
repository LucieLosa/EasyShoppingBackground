from django.contrib import admin

from bazaar.models import Event, EventUser, EventSeller


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


@admin.register(EventSeller)
class EventSellerAdmin(admin.ModelAdmin):
    list_display = [
        "identifier", "seller", 'total_sold_items', "total_sales_amount", "total_fees", "is_no_fees", "event", ]
    list_filter = ("event", "is_no_fees")
    readonly_fields = ['total_sold_items', "total_sales_amount", "total_fees"]
    exclude = ("x_user",)
