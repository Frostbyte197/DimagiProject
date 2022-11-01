from django.contrib import admin
from django.urls import path, include

base_url = 'api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(base_url, include('djoser.urls')),
    path(base_url, include('djoser.urls.authtoken')),
    path(base_url, include('apps.location.urls'))
]
