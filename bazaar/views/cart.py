import re

from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import generics, permissions, authentication
from rest_framework.response import Response
from rest_framework.views import APIView

from bazaar.models import Event, Cart, Item, EventSeller
from bazaar.serializers.event import EventsSerializer


class AddCart(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    CARTID_REGEX = r"([A-Z]*)\d*"

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        event = Event.objects.filter(is_active=True).order_by('-date').first()
        try:
            cart_match = re.match(self.CARTID_REGEX, kwargs.get("cartId"))
            matched_user = User.objects.filter(easho_user__prefix=cart_match[1]).first()
            x_user = matched_user or request.user
            cart_identifier = kwargs.get("cartId")
            while (Cart.objects.filter(identifier=cart_identifier, event=event).first()):
                cart_identifier = "D" + cart_identifier
            cart = Cart.objects.create(
                identifier=cart_identifier,
                event=event,
                user=x_user,
                x_user=x_user
            )

        except Exception as e:
            return Response({'status': "Integrity ERROR"})

        errors = []
        items = []
        for req_item in request.data:
            try:
                seller_identifier = req_item.get("seller")
                try:
                    event_seller = EventSeller.objects.get(identifier=seller_identifier, event=event)
                except EventSeller.DoesNotExist:
                    event_seller = EventSeller.create_if_not_found(seller_identifier, event)

                items.append(Item(
                    cart=cart,
                    event_seller=event_seller,
                    order=(req_item.get("order") or 0),
                    price=req_item.get("price"),
                    x_user=x_user
                ))
            except Exception as e:
                errors.append(str(e))
        Item.objects.bulk_create(items)
        if errors:
            return Response({'status': ",".join(errors)})

        return Response({'status': "OK"})


# TODO
class EditCart(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Event.objects.prefetch_related("sellers").all()
    serializer_class = EventsSerializer
