from django.urls import path
from . import views

urlpatterns = [
    path('funcionarios/',views.employees, name='employees'),
    path('funcionarios/atualizar', views.update_employees, name='update_employees'),
    path('funcionarios/lider', views.update_employees_leader, name='update_employees_leader'),
    path('funcionarios/setor', views.update_employees_sector, name='update_employees_sector'),
    path('hora_extra/',views.extra_hour, name='extra_hour'),
    path('hora_extra/atualizar', views.update_extra_hour, name='update_extra_hour'),
    path('hora_extra/zerar_hora_extra', views.reset_extra_hours, name='reset_extra_hours'),
    path('limite_hora_extra', views.extra_hour_limit, name='extra_hour_limit'),
    path('limite_hora_extra/atualizar', views.update_extra_hour_limit, name='update_extra_hour_limit'),
    path('hora_extra/limit_hora_extra_por_mes', views.update_extra_hour_month, name='update_extra_hour_month'),
]