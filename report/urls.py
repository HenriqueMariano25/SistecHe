from django.urls import path
from . import views

urlpatterns = [
    path('',views.report_shift, name='report_shift'),
]