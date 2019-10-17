from django.urls import path
from rest_framework.routers import DefaultRouter

from events import views

router = DefaultRouter()
router.register(r'', views.EventViewset, basename='event')

urlpatterns = router.urls + [
    path('<int:pk>/register', views.RegisterView.as_view(), name='api_register')
]
