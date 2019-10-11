from rest_framework.routers import DefaultRouter

from events import views

router = DefaultRouter()
router.register(r'', views.EventViewset, basename='event')

urlpatterns = router.urls
