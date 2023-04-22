
from django.urls import path, include

from blackpearl.associados import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastrar/', views.cadastrardjango, name='cadastrar'),
    path('importExcel/', views.importExcel, name='importExcel'),
    path('<int:associado_id>', views.visualizar, name='visualizar'),
    path('editar/<int:associado_id>/', views.editar, name='editar'),
    path('excluir/<int:associado_id>/', views.excluir, name='excluir'),
]
