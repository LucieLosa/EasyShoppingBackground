from django.contrib import admin

from bazaar.models import Seller


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ["nickname", 'default_identifier',  "email", "phone", "is_active", "is_no_fees_default"]
    list_filter = ("is_active", "is_no_fees_default",)
    exclude = ("x_user",)
