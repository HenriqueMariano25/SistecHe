from django.urls import path
from . import views

urlpatterns = [
    path('diretor',views.approval_director,name='approval_director'),
    path('diretor/lista',views.director_list,name='director_list'),
    path('aprovacao',views.approval_scheduluing,name='approval_scheduluing'),
]