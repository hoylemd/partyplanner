from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.views.generic import (
    DetailView, ListView, CreateView, RedirectView, UpdateView
)
from django.urls import reverse_lazy
from django.db import IntegrityError

from rest_framework import viewsets

from events.models import Event
from events.serializers import EventSerializer
from events.permissions import ObjectOwnership


class EventViewset(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [ObjectOwnership]

    def perform_create(self, serializer):
        """On create, set the owner to the request user"""
        serializer.save(owner=self.request.user)


class OwnerOnlyAccessMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_object().owner:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class EventList(ListView):
    model = Event
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EventDetail(DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        event = context['event']

        context['user_may_register'] = (
            not user.is_anonymous
            and user.pk not in event.attendance_set.values_list('user', flat=True)
        )

        return context


class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    fields = (
        'name', 'description', 'starts_at', 'ends_at', 'image'
    )

    def form_valid(self, form):
        form.instance.owner = self.request.user

        return super().form_valid(form)


class EventEdit(LoginRequiredMixin, OwnerOnlyAccessMixin, UpdateView):
    model = Event
    fields = (
        'name', 'description', 'starts_at', 'ends_at', 'image'
    )


class Register(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, **kwargs):
        return reverse_lazy('event_detail', kwargs=kwargs)

    def post(self, request, **kwargs):
        event = Event.objects.get(pk=kwargs['pk'])

        try:
            record = event.attendance_set.create(user=request.user)
        except IntegrityError:
            # a record already exists, so just delete it
            record = event.attendance_set.get(user=request.user)
            record.delete()

        return super().post(request, **kwargs)
