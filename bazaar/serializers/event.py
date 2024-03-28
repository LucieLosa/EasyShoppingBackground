from rest_framework import serializers
from bazaar.models import Event


class EventsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ["id", "name", "date", "is_active", "is_closed", "notes", "fee_value_default"]
