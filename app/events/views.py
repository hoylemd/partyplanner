from django.views.generic import DetailView, ListView, CreateView

from events.models import Event


class EventList(ListView):
    model = Event
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EventDetail(DetailView):
    model = Event


class EventCreate(CreateView):
    model = Event
    fields = (
        'name', 'description', 'starts_at', 'ends_at', 'image'
    )

    def form_valid(self, form):
        form.instance.owner = self.request.user

        return super().form_valid(form)
