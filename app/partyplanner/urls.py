from django.contrib import admin
from django.urls import include, path

from partyplanner.views import Login, Logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),
    path('', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]
