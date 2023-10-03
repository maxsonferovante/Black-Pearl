from django.conf import settings
from django.conf.urls.static import static
from django.template.defaulttags import url
from django.urls import path, include

from blackpearl.convenios import views
from blackpearl.convenios.views import HomeTemplateView, VerificarDependentesView, ContratoPlanoOdontologico, \
    ContratoPlanoOdontologicoCreateView, ContratoPlanoOdontologicoDetailView, ContratoPlanoOdontologicoUpdateView, \
    ContratoPlanoOdontologicoDeleteView, ContratoOdontologicaListView, VerificarAssociacaoView, \
    ContratoOdontologicaDependenteCreateView, ContratoOdontologicaDependenteListView, \
    ContratoOdontologicaDependenteUpdateView, ContratoOdontologicaDependenteDeleteView, VerificarAssociacaoDependente, \
    ContratoPlanoSaudeCreateView, ContratoPlanoSaudeListView, ContratoPlanoSaudeUpdateView, \
    ContratoPlanoSaudeDeleteView, ContratoPlanoSaudeDetailView, ConsultaValorFaixaEtaria, \
    ContratoPlanoSaudeDependenteCreateView, ConsultaValorFaixaEtariaDependente
from blackpearl.convenios.views import CartaoListView, CartaoCreateView, CartaoUpdateView, CartaoDetailView, CartaoDeleteView
from blackpearl.convenios.views import FaturaCreateView, FaturaListView, FaturaDeleteView, FaturaUpdateView


urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home_conv'),
    path('cadastrarcartao/', CartaoCreateView.as_view(), name ='cartao_cadastrar'),
    path('detalhescartao/<int:pk>/', CartaoDetailView.as_view(), name ='cartao_visualizar'),
    path('editarcartao/<int:pk>/', CartaoUpdateView.as_view(), name ='cartao_editar'),
    path('excluircartao/<int:pk>/', CartaoDeleteView.as_view(), name ='cartao_excluir'),
    path('listagemcartoes/', CartaoListView.as_view(), name ='listagemcartoes'),

    path('editarfatura/<int:pk>/', FaturaUpdateView.as_view(), name ='fatura_editar'),
    path('excluirfatura/<int:pk>/', FaturaDeleteView.as_view(), name ='fatura_excluir'),
    path('cadastrarfatura/', FaturaCreateView.as_view(), name ='fatura_cadastrar'),
    path('listagemfaturas/', FaturaListView.as_view(), name ='listagemfaturas'),

    path('contratoodontologica/', ContratoPlanoOdontologicoCreateView.as_view(), name='contratoodontologica_cadastrar'),
    path('contratoodontologica/<int:pk>/detalhes/', ContratoPlanoOdontologicoDetailView.as_view(),name='contratoodontologico_visualizar'),
    path('contratoodontologica/<int:pk>/editar/', ContratoPlanoOdontologicoUpdateView.as_view(),name='contratoodontologico_editar'),
    path('contratoodontologica/<int:pk>/excluir', ContratoPlanoOdontologicoDeleteView.as_view(),name='contratoodontologico_excluir'),
    path('listagemcontratoodontologica/', ContratoOdontologicaListView.as_view(), name='listagemcontratoodontologica'),

    path('verificardependentes/', VerificarDependentesView.as_view(), name='verificar_dependentes'),
    path('contratoodontologica/verificarassociacao/', VerificarAssociacaoView.as_view(), name='verificar_associacao'),

    path('planoodontologico/add/dependente', ContratoOdontologicaDependenteCreateView.as_view(), name='cadastrar_dependentes_contrato_plano_odont'),
    path('planoodontologico/all/dependentes', ContratoOdontologicaDependenteListView.as_view(), name='listar_dependentes_contrato_plano_odont'),
    path('planoodontologico/<int:pk>/dependente', ContratoOdontologicaDependenteUpdateView.as_view(), name='editar_dependentes_contrato_plano_odonto'),
    path('planoodontologico/<int:pk>/dependente', ContratoOdontologicaDependenteDeleteView.as_view(), name='excluir_dependentes_contrato_plano_odonto'),
    path('contratoodontologica/verificarassociacaodependente/', VerificarAssociacaoDependente.as_view(), name='verificar_associacao_dependente'),


    path('contratoplanosaude/add', ContratoPlanoSaudeCreateView.as_view(), name='cadastrar_contrato_plano_saude'),
    path('contratoplanosaude/all', ContratoPlanoSaudeListView.as_view(), name='listar_contratos_plano_saude'),
    path('contratoplanosaude/<int:pk>/editar', ContratoPlanoSaudeUpdateView.as_view(), name='editar_contrato_plano_saude'),
    path('contratoplanosaude/<int:pk>/excluir', ContratoPlanoSaudeDeleteView.as_view(), name='excluir_contrato_plano_saude'),
    path('contratoplanosaude/<int:pk>/detalhes', ContratoPlanoSaudeDetailView.as_view(), name='detalhes_contrato_plano_saude'),
    path('contratoplanosaude/consultafaixa/', ConsultaValorFaixaEtaria.as_view(), name='consultafaixa'),
    path('contratoplanosaude/consultafaixa_dependente/', ConsultaValorFaixaEtariaDependente.as_view(), name='consulta_faixa_dependente'),

    path('contratoplanosaude/add/dependente', ContratoPlanoSaudeDependenteCreateView.as_view(), name='cadastrar_dependentes_contrato_plano_saude'),


    path('exportar/', views.exportar, name = 'exportar'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)