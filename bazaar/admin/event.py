import csv

from django import forms
from django.contrib import admin
from django.http import HttpResponse
from django.utils.translation import gettext as _
from import_export.admin import ImportExportActionModelAdmin
from import_export.fields import Field
from import_export.forms import ImportForm, ConfirmImportForm
from import_export.resources import ModelResource

from bazaar.models import Event, EventUser, EventSeller, Item


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


class EventSellerResource(ModelResource):
    """
    Custom import fields - Username, seller number
    """
    event = None
    force_init_instance = True
    seller = Field(attribute='seller__name')

    def __init__(self, user, **kwargs):
        super().__init__()
        self.x_user = user

    def before_import(self, dataset, **kwargs):
        super().before_import(dataset, **kwargs)
        self.event = kwargs.get("event")

    def skip_row(self, instance, original, row, import_validation_errors=None):
        identifier = row.get("identifier")
        username = row.get("username").strip()
        if EventSeller.objects.filter(event=self.event, seller__nickname=username, identifier=identifier).first():
            return True
        event_seller = EventSeller.objects.filter(event=self.event, identifier=identifier).first()
        if event_seller:
            # original = event_seller
            # TODO
            import_validation_errors['identifier'] = f"Identifier {identifier} for this event already exists"
        return super().skip_row(instance, original, row, import_validation_errors=import_validation_errors)

    def before_save_instance(self, instance, row, **kwargs):
        from bazaar.models import Seller
        identifier = row.get("identifier")
        nickname = row.get("username").strip()
        seller = Seller.objects.filter(nickname=nickname, default_identifier=identifier).first()
        if not seller:
            seller = Seller.objects.filter(nickname=nickname).first()
        if not seller:
            seller = Seller.objects.create(
                nickname=nickname, name=nickname, default_identifier=identifier, notes="Seller was created from import")
        instance.event = self.event
        instance.seller = seller
        instance.is_no_fees = seller.is_no_fees_default
        instance.x_user_id = self.x_user.pk

    # list_display = [
    #     "identifier", "seller", 'total_sold_items', "total_sales_amount", "total_fees", "is_no_fees", "event", ]
    class Meta:
        model = EventSeller
        fields = ("identifier", "seller")
        name = _("Import list of event sellers as first column of seller number and second column as seller name")
        force_init_instance = True


class CustomImportForm(ImportForm):
    event = forms.ModelChoiceField(
        queryset=Event.objects.all(),
        required=True)


class CustomConfirmImportForm(ConfirmImportForm):
    event = forms.ModelChoiceField(
        queryset=Event.objects.all(),
        required=True)


@admin.register(EventSeller)
class EventSellerAdmin(ImportExportActionModelAdmin):
    resource_classes = [EventSellerResource]
    import_form_class = CustomImportForm
    confirm_form_class = CustomConfirmImportForm

    list_display = [
        "identifier", "seller", 'total_sold_items', "total_sales_amount", "total_fees", "is_no_fees", "event", ]
    list_filter = ("event", "is_no_fees")
    readonly_fields = ['total_sold_items', "total_sales_amount", "total_fees"]
    exclude = ("x_user",)
    inlines = (
        ItemInlineAdmin,
    )
    actions = ["export_as_csv"]

    def get_confirm_form_initial(self, request, import_form):
        initial = super().get_confirm_form_initial(request, import_form)
        # Pass on the `event` value from the import form to
        # the confirm form (if provided)
        if import_form:
            initial['event'] = import_form.cleaned_data['event'].id
        return initial

    def get_import_data_kwargs(self, request, *args, **kwargs):
        """
        Prepare kwargs for import_data.
        """
        form = kwargs.get("form", None)
        if form and hasattr(form, "cleaned_data"):
            kwargs.update({"event": form.cleaned_data.get("event", None)})
        return kwargs

    def get_import_resource_kwargs(self, request, **kwargs):
        kwargs = super().get_resource_kwargs(request, **kwargs)
        kwargs.update({"user": request.user})
        return kwargs

    def after_init_instance(self, instance, new, row, **kwargs):
        if "event" in kwargs:
            instance.event = kwargs["event"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        # field_names = [field.name for field in meta.fields]
        field_names = [
            "identifier", "seller_name", "total_sales_amount", "fee_value_percentage", "total_payout",
            "total_sold_items"]
        field_names_header = [
            _("Number"), _("Seller name"), _("Totally earned"), "10%", _("To payout"), _("Sold items")
        ]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names_header)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = _("Export event sellers")
