from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy


class Event(models.Model):
    """
    Represents a planned event
    """
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    # intended to be a url to an image
    image = models.CharField(max_length=255, blank=True)

    def get_absolute_url(self):
        return reverse_lazy('event_detail', kwargs={'pk': self.pk})


class Attendance(models.Model):
    """
    Represents a user registering to an event
    """
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
