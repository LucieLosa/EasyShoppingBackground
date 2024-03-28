import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _

from .base import BaseModel
from .seller import Seller


class Event(BaseModel):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, verbose_name=_("name"))
    short_name = models.CharField(max_length=16, verbose_name=_('short name'))
    date = models.DateTimeField(verbose_name=_("date"))
    is_active = models.BooleanField(default=False, verbose_name=_("Active"))
    is_closed = models.BooleanField(default=False, verbose_name=_("Closed"))
    notes = models.TextField(verbose_name=_("Notes"), blank=True)
    fee_value_default = models.PositiveSmallIntegerField(verbose_name=_("Static fee value default"), default=0)
    fee_value_percentage = models.PositiveSmallIntegerField(verbose_name=_("Percentage fee value default"), default=0)
    # users = models.ManyToManyField(User, through='EventsUsers', related_name="events_user")
    sellers = models.ManyToManyField(Seller, through='EventSeller')
    x_created = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("Created"))
    x_modified = models.DateTimeField(auto_now=True)
    x_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="events_x_user")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        ordering = ["-date"]


class EventUser(BaseModel):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    x_created = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("Created"))
    x_modified = models.DateTimeField(auto_now=True)
    x_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="x_user")

    def __str__(self):
        return f'{self.event.short_name} - {self.user}'

    class Meta:
        ordering = ["event", "user"]
        unique_together = [["event", "user"]]
        verbose_name = _("Event user")
        verbose_name_plural = _("Event users")


class EventSeller(BaseModel):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event")
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="seller")
    identifier = models.PositiveSmallIntegerField(verbose_name=_("Seller identifier"))
    is_no_fees = models.BooleanField(default=False, verbose_name=_("No fees"))
    total_sold_items = models.PositiveSmallIntegerField(default=0, verbose_name=_("Total sold items"))
    total_sales_amount = models.PositiveSmallIntegerField(default=0, verbose_name=_("Total sales amount"))
    total_fees = models.PositiveSmallIntegerField(default=0, verbose_name=_("Total Fees"))

    x_created = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("Created"))
    x_modified = models.DateTimeField(auto_now=True)
    x_user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.event.short_name} - {self.identifier}"

    class Meta:
        ordering = ["event", "seller"]
        unique_together = [["event", "seller"], ["event", "identifier"]]
        verbose_name = _("Event seller")
        verbose_name_plural = _("Event sellers")

    @staticmethod
    def create_if_not_found(identifier, event):

        nickname = f'{Seller.NOT_FOUND}_{identifier}'
        seller, created = Seller.objects.get_or_create(default_identifier=identifier, nickname=nickname)
        not_found_event_seller, created = EventSeller.objects.get_or_create(seller=seller, identifier=identifier, event=event)
        return not_found_event_seller
