from django.urls import path
from events import views

urlpatterns = [
    path('', views.EventList.as_view(), name='event_list'),
    path('<int:pk>/', views.EventDetail.as_view(), name='event_detail'),
    path('new/', views.EventCreate.as_view(), name='event_create'),
    path('<int:pk>/register', views.Register.as_view(), name='register'),
    path('<int:pk>/edit', views.EventEdit.as_view(), name='event_edit'),
]
