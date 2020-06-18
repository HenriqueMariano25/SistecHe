from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('start.urls')),
    path('importacao/', include('imports.urls')),
    path('usuario/', include('users.urls')),
    path('agendamento/', include('scheduling.urls')),
    path('relatorio/', include('report.urls')),
    path('aprovacao/', include('approval.urls')),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
