from django.contrib import admin
from django.urls import include, path
from rest_framework_jwt.views import obtain_jwt_token

from partyplanner import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),

    path('', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),

    path('users/', views.UserList.as_view(), name='signup'),
    path('whoami/', views.CurrentUser.as_view(), name='whoami'),
    path('token-auth/', obtain_jwt_token),
]
