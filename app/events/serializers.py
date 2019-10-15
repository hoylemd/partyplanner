from django.utils.dateparse import parse_datetime
from rest_framework import serializers

from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    def validate_ends_at(self, value):
        try:
            start_time_raw = self.initial_data['starts_at']
            start_time = parse_datetime(start_time_raw)
            start_time = start_time.astimezone()  # make it UTC tz-aware
        except KeyError:
            # starts_at not submitted, check the instance
            try:
                start_time = self.instance.starts_at
            except AttributeError:
                # instance doesn't exist, this is a create
                # just pass it - starts_at validation will catch the error
                return value

        if value < start_time:
            raise serializers.ValidationError('End time before start time.')

        return value

    class Meta:
        model = Event
        fields = (
            'pk', 'created_at', 'owner_id', 'name', 'description',
            'starts_at', 'ends_at', 'image'
        )
