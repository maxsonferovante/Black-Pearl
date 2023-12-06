from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from blackpearl.cobrancas.views.homeView import FaturaCobrancaListView
from blackpearl.cobrancas.views.faturaCobrancaGeracaoView import FaturaCobrancaGeracaoView, \
    FaturaCobrancaGeracaoContratoPlanoSaudeCreateView, FaturaCobrancaGeracaoContratoPlanoOdontologicoCreateView, \
    FaturaCobrancaGeracaoContratoPlanoSaudeColetivaView, FaturaCobrancaGeracaoContratoPlanoOdontologicoColetivaView, \
    FaturaCobrancaGeracaoConsultaValorContratoIndividualView


urlpatterns = [
    path('relatorios/', FaturaCobrancaListView.as_view(), name='home_cob'),
    path('gerar/', FaturaCobrancaGeracaoView.as_view(), name='gerar_cob'),

    path('gerar/planodesaude/contrato/individual/', FaturaCobrancaGeracaoContratoPlanoSaudeCreateView.as_view(), name='gerar_cob_planodesaude_contrato'),
    path('gerar/planoodontologico/contrato/individual/', FaturaCobrancaGeracaoContratoPlanoOdontologicoCreateView.as_view(), name='gerar_cob_planoodontologico_contrato'),
    path('gerar/contrato/individual/consulta/valor/', FaturaCobrancaGeracaoConsultaValorContratoIndividualView.as_view(), name='gerar_cob_contrato_individual_consulta_valor'),
    path('gerar/planodesaude/contrato/coletiva/', FaturaCobrancaGeracaoContratoPlanoSaudeColetivaView.as_view(), name='gerar_cob_planodesaude_contrato_coletiva'),
    path('gerar/planoodontologico/contrato/coletiva/', FaturaCobrancaGeracaoContratoPlanoOdontologicoColetivaView.as_view(), name='gerar_cob_planoodontologico_contrato_coletiva'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)