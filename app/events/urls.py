from django.urls import path
from events.views import EventList, EventDetail

urlpatterns = [
    path('', EventList.as_view(), name='event_list'),
    path('<int:pk>/', EventDetail.as_view(), name='event_detail'),
]
