from django.urls import path
from . import views

urlpatterns = [
    path('funcionarios/',views.employees, name='employees'),
    path('funcionarios/atualizar', views.update_employees, name='update_employees'),
    path('funcionarios/lider', views.update_employees_leader, name='update_employees_leader'),
    path('funcionarios/setor', views.update_employees_sector, name='update_employees_sector'),
    path('hora_extra/',views.extra_hour, name='extra_hour')
]