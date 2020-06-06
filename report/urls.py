from django.urls import path
from . import views

urlpatterns = [
    path('por_turno',views.report_shift, name='report_shift'),
    path('por_turno/preview',views.shift_preview, name='shift_preview'),
]