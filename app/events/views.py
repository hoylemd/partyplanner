from django.views.generic import DetailView, ListView

from events.models import Event


class EventList(ListView):
    model = Event
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EventDetail(DetailView):
    model = Event
