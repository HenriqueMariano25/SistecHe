from django.urls import path
from . import views

urlpatterns = [
    path('effective/',views.effective, name='effective'),
]