
from django.urls import path, include, re_path

from blackpearl.associados import views
from blackpearl.associados.views import HomeTemplateView, AssociadoUpdateView, AssociadoDeleteView, AssociadoDetailView, \
    AssociadoCreateView, DependenteCreateView

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home_assoc'),
    path('<int:pk>/', AssociadoDetailView.as_view(), name='visualizar'),
    path('editar/<int:pk>/', AssociadoUpdateView.as_view(), name='editar'),
    path('excluir/<int:pk>/', AssociadoDeleteView.as_view(), name='excluir'),

    path('cadastrar/', AssociadoCreateView.as_view(), name='cadastrar'),
    path('cadastrardependentes/', DependenteCreateView.as_view(), name='cadastrardependentes'),
    ##path('importExcel/', views.importExcel, name='importExcel'),

]
