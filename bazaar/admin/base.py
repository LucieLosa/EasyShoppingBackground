from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from bazaar.models.base import EashoUser


class EashoUserInline(admin.StackedInline):
    model = EashoUser
    can_delete = False
    verbose_name_plural = "easho"
    fields = ("prefix",)


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "get_prefix", "email", "first_name", "last_name", "is_staff")
    inlines = [EashoUserInline]

    def get_prefix(self, obj):
        return obj.easho_user.prefix

    get_prefix.short_description = "Prefix"


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
