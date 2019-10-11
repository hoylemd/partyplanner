from datetime import datetime

from rest_framework import serializers

from events.models import Event

ISO_8601_FORMAT = r'%Y-%m-%d %H:%M:%S'


class EventSerializer(serializers.ModelSerializer):
    def validate_ends_at(self, value):
        start_time_raw = self.initial_data['starts_at']
        start_time = datetime.strptime(start_time_raw, ISO_8601_FORMAT)
        start_time = start_time.astimezone()  # make it UTC tz-aware
        if value < start_time:
            raise serializers.ValidationError('End time before start time.')

        return value

    class Meta:
        model = Event
        fields = (
            'pk', 'created_at', 'owner_id', 'name', 'description',
            'starts_at', 'ends_at', 'image'
        )
