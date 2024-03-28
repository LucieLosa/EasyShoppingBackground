from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db import transaction
from rest_framework import generics, permissions, authentication
from rest_framework.response import Response
from rest_framework.views import APIView

from bazaar.models import Event, Cart, Item, EventSeller
from bazaar.serializers.event import EventsSerializer


class AddCart(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        event = Event.objects.filter(is_active=True).order_by('-date').first()

        try:

            cart = Cart.objects.create(
                identifier=kwargs.get("cartId"),
                event=event,
                user=request.user
            )

        except IntegrityError:
            return Response({'status': "Integrity ERROR"})

        errors = []

        for req_item in request.data:
            try:
                seller_identifier = req_item.get("seller")
                try:
                    event_seller = EventSeller.objects.get(identifier=seller_identifier, event=event)
                except EventSeller.DoesNotExist:
                    event_seller = EventSeller.create_if_not_found(seller_identifier, event)

                Item.objects.create(
                    cart=cart,
                    event_seller=event_seller,
                    price=req_item.get("price"),
                    size=req_item.get("size")
                )
            except Exception as e:
                errors.append(str(e))

        if errors:
            return Response({'status': ",".join(errors)})

        return Response({'status': "OK"})


# TODO
class EditCart(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Event.objects.prefetch_related("sellers").all()
    serializer_class = EventsSerializer
