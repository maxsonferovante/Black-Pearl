from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView

from blackpearl.cobrancas.models.faturaCobrancaModels import CobrancaPlanoSaude, CobrancaPlanoOdontologico
from blackpearl.cobrancas.forms.faturaCobrancaGeracaoForm import FaturaCobrancaGeracaoContratoPlanoSaudeForm, \
    FaturaCobrancaGeracaoContratoPlanoOdontologicoForm


@method_decorator(login_required, name='dispatch')
class FaturaCobrancaGeracaoView(TemplateView):
    template_name = 'cobrancas/gerar_cob.html'


@method_decorator(login_required, name='dispatch')
class FaturaCobrancaGeracaoContratoPlanoSaudeCreateView(CreateView):
    model = CobrancaPlanoSaude
    form_class = FaturaCobrancaGeracaoContratoPlanoSaudeForm
    template_name = 'cobrancas/gerar_cob_planodesaude_contrato.html'
    success_url = reverse_lazy('home_cob')


@method_decorator(login_required, name='dispatch')
class FaturaCobrancaGeracaoContratoPlanoOdontologicoCreateView(CreateView):
    model = CobrancaPlanoOdontologico
    form_class = FaturaCobrancaGeracaoContratoPlanoOdontologicoForm
    template_name = 'cobrancas/gerar_cob_planoodontologico_contrato.html'
    success_url = reverse_lazy('home_cob')
