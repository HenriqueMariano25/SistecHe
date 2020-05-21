from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('start.urls')),
    path('imports/', include('imports.urls')),
    path('admin/', admin.site.urls),
]
