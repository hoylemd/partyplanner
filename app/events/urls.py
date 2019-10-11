from django.urls import path
from rest_framework.routers import DefaultRouter

from events import views

router = DefaultRouter()
router.register(r'', views.EventViewset, basename='event')

urlpatterns = [
    path('', views.EventList.as_view(), name='event_list'),
    path('<int:pk>/', views.EventDetail.as_view(), name='event_detail'),
    path('new/', views.EventCreate.as_view(), name='event_create'),
    path('<int:pk>/register', views.Register.as_view(), name='register'),
    path('edit/<int:pk>', views.EventEdit.as_view(), name='event_edit'),
]
