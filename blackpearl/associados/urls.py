
from django.urls import path, include, re_path

from blackpearl.associados import views
from blackpearl.associados.views import HomeTemplateView, AssociadoUpdateView, AssociadoDeleteView, AssociadoDetailView, \
    AssociadoCreateView, DependenteCreateView, DependenteUpdateView, DependenteDeleteView, ImportExcelView, \
    ConsultaIdadeAssocView

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home_assoc'),
    path('<int:pk>/', AssociadoDetailView.as_view(), name='visualizar_associado'),
    path('editar/<int:pk>/', AssociadoUpdateView.as_view(), name='editar_associado'),
    path('excluir/<int:pk>/', AssociadoDeleteView.as_view(), name='excluir_associado'),
    path('cadastrar/', AssociadoCreateView.as_view(), name='cadastrar_associado'),

    path('idadeassoc/consulta/', ConsultaIdadeAssocView.as_view(), name='consulta_data_nascimento_assoc'),
    path('cadastrardependentes/', DependenteCreateView.as_view(), name='cadastrar_dependentes'),
    path('editardependente/<int:pk>/', DependenteUpdateView.as_view(), name='editar_dependente'),
    path('excluirdependente/<int:pk>/', DependenteDeleteView.as_view(), name='excluir_dependente'),

    ##path('importExcel/', views.importExcel, name='importExcel'),
    path('importExcel/', ImportExcelView.as_view(), name='importExcel'),

]
