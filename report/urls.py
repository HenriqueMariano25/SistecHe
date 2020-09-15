from django.urls import path
from . import views

urlpatterns = [
    path('por_turno', views.report_shift, name='report_shift'),
    path('por_turno/preview', views.shift_preview, name='shift_preview'),
    path('por_turno/pdf', views.shift_pdf, name='shift_pdf'),
    path('por_turno/excel', views.generate_excel_shift, name='generate_excel_shift'),
    path('por_lider', views.report_leader, name='report_leader'),
    path('por_lider/preview', views.leader_preview, name='leader_preview'),
    path('por_lider/pdf', views.leader_pdf, name='leader_pdf'),
    path('por_lider/excel', views.generate_excel_leader, name='generate_excel_leader'),
    path('por_turno/teste', views.shift_pdf, name='teste'),
]
