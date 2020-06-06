from django.urls import path
from . import views

urlpatterns = [
    path('',views.scheduling_employees, name='scheduling_employees'),
    path('agendamento/lider_selecionado',views.selected_leader, name='selected_leader'),
    path('agendamento/agendar',views.finalize_employee_scheduling, name='finalize_employee_scheduling'),
    path('buscar',views.search_employee_scheduling, name='search_employee_scheduling'),
]