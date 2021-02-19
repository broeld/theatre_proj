from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('plays.urls', namespace='plays')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
]
