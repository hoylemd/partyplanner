from django.urls import path
from events.views import EventList, EventDetail, EventCreate, Register

urlpatterns = [
    path('', EventList.as_view(), name='event_list'),
    path('<int:pk>/', EventDetail.as_view(), name='event_detail'),
    path('new/', EventCreate.as_view(), name='event_create'),
    path('<int:pk>/register', Register.as_view(), name='register'),
]
