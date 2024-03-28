from rest_framework import generics, permissions  # new

from bazaar.models import Event
from bazaar.serializers.event import EventsSerializer


class EventsList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventsSerializer
    lookup_url_kwarg = "pk"


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Event.objects.prefetch_related("sellers").all()
    serializer_class = EventsSerializer
