from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from blackpearl.cobrancas.views.homeView import FaturaCobrancaListView
from blackpearl.cobrancas.views.faturaCobrancaGeracaoView import FaturaCobrancaGeracaoView, FaturaCobrancaGeracaoContratoPlanoSaudeCreateView, FaturaCobrancaGeracaoContratoPlanoOdontologicoCreateView

urlpatterns = [
    path('relatorios/', FaturaCobrancaListView.as_view(), name='home_cob'),
    path('gerar/', FaturaCobrancaGeracaoView.as_view(), name='gerar_cob'),
    path('gerar/planodesaude/contrato/', FaturaCobrancaGeracaoContratoPlanoSaudeCreateView.as_view(), name='gerar_cob_planodesaude_contrato'),
    path('gerar/planoodontologico/contrato/', FaturaCobrancaGeracaoContratoPlanoOdontologicoCreateView.as_view(), name='gerar_cob_planoodontologico_contrato'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)