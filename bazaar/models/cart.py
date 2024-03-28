import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _

from .base import BaseModel
from .event import Event, EventSeller


class Cart(BaseModel):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    identifier = models.CharField(max_length=128, verbose_name=_("Name"))
    event = models.ForeignKey(Event, on_delete=models.PROTECT, verbose_name=_("bazaar"))
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="carts_user")
    is_checked = models.BooleanField(verbose_name=_("Cart checked"), default=False)

    x_created = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("Created"))
    x_modified = models.DateTimeField(auto_now=True)
    x_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="carts_x_user")

    def __str__(self):
        return f"{self.identifier}"

    def items_count(self):
        return self.items.count()

    def total_price(self):
        return self.items.aggregate(summary=Sum("price")).get('summary')

    total_price.short_description = _("Sum")

    class Meta:
        ordering = ["event", "identifier"]
        unique_together = [["identifier", "event"]]
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")


class Item(BaseModel):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name=_("Cart"), related_name="items")
    event_seller = models.ForeignKey(EventSeller, on_delete=models.PROTECT, related_name="event_seller")
    size = models.CharField(max_length=32, verbose_name=_("Size"), null=True, blank=True)
    price = models.PositiveSmallIntegerField(verbose_name=_("Price"), default=0)
    x_created = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("Created"))
    x_modified = models.DateTimeField(auto_now=True)
    x_user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.cart} {self.event_seller}"

    class Meta:
        ordering = ["cart", "event_seller", "price"]
        verbose_name = _("Item")
        verbose_name_plural = _("Items")


@receiver(post_save, sender=Item)
def my_handler(sender, **kwargs):
    item = kwargs.get("instance")
    if item.event_seller:
        total_sales_amount = Item.objects.filter(event_seller=item.event_seller).aggregate(
            Sum('price'))['price__sum']
        total_sold_items = Item.objects.filter(event_seller=item.event_seller).count()
        item.event_seller.total_sales_amount = total_sales_amount
        item.event_seller.total_sold_items = total_sold_items
        if not item.event_seller.is_no_fees:
            item.event_seller.total_fees = (
                                                   item.event_seller.event.fee_value_percentage / 100 * total_sales_amount
                                           ) + item.event_seller.event.fee_value_default
        item.event_seller.save(update_fields=["total_fees", "total_sales_amount", "total_sold_items"])
