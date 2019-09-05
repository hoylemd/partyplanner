from rest_framework import serializers
from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'pk', 'created_at', 'owner_id', 'name', 'description',
            'starts_at', 'ends_at', 'image'
        )
