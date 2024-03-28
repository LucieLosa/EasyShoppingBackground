import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _

from bazaar.models.base import BaseModel


class Seller(BaseModel):
    NOT_FOUND = "nenalezen"

    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    nickname = models.CharField(max_length=128, verbose_name=_("Unique nickname - quick find"), unique=True)
    name = models.CharField(max_length=128, verbose_name=_("Name"), blank=True)
    email = models.CharField(max_length=128, verbose_name=_("Email"), blank=True)
    phone = models.CharField(max_length=128, verbose_name=_("Phone"), blank=True)  # TODO phone number
    notes = models.TextField(verbose_name=_("Notes"), blank=True)
    default_identifier = models.PositiveSmallIntegerField(verbose_name=_("Seller number (default setting)"), null=True)
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    is_no_fees_default = models.BooleanField(default=False, verbose_name=_("No fees (default setting)"))

    x_created = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("Created"))
    x_modified = models.DateTimeField(auto_now=True)
    x_user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.nickname}"

    class Meta:
        ordering = ["nickname"]
        verbose_name = _("Seller")
        verbose_name_plural = _("Sellers")
