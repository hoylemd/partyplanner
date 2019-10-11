from django.contrib import admin
from django.urls import include, path
from rest_framework_jwt.views import obtain_jwt_token

from partyplanner import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),

    path('', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('signup/', views.Signup.as_view(), name='signup'),

    # API routes
    path('api/users/', views.UserList.as_view(), name='user_list'),
    path('api/whoami/', views.CurrentUser.as_view(), name='whoami'),
    path('api/token-auth/', obtain_jwt_token),
    path('api/events/', include('events.api_urls')),
]
