from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from blackpearl.convenios.views import HomeTemplateView, CartaoListView, CartaoCreateView, FaturaCreateView, \
    FaturaListView, ContratacaoOdontologicaCreateView, ContratacaoOdontologicaListView, \
    VerificarDependentesView

from blackpearl.convenios import views
urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home_conv'),
    path('cadastrarcartao/', CartaoCreateView.as_view(), name ='cartao_cadastrar'),
    path('listagemcartoes/', CartaoListView.as_view(), name ='listagemcartoes'),
    path('cadastrarfatura/', FaturaCreateView.as_view(), name ='fatura_cadastrar'),
    path('listagemfaturas/', FaturaListView.as_view(), name ='listagemfaturas'),
    path('contratacaoodontologica/', ContratacaoOdontologicaCreateView.as_view(), name='contratacaoodontologica_cadastrar'),
    path('listagemcontratacaoodontologica/', ContratacaoOdontologicaListView.as_view(), name='listagemcontratacaoodontologica'),

    path('verificardependentes/', VerificarDependentesView.as_view(), name='verificar_dependentes'),


    path('exportar/', views.exportar, name = 'exportar'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)