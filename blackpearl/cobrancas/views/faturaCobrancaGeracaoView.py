from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView

from blackpearl.cobrancas.models.faturaCobrancaModels import CobrancaPlanoSaude, CobrancaPlanoOdontologico
from blackpearl.cobrancas.forms.faturaCobrancaGeracaoForm import FaturaCobrancaGeracaoContratoPlanoSaudeForm, \
    FaturaCobrancaGeracaoContratoPlanoOdontologicoForm

from blackpearl.cobrancas.services.processoFaturamentoService import ProcessoFaturamentoService


@method_decorator(login_required, name='dispatch')
class FaturaCobrancaGeracaoView(TemplateView):
    processamento_faturamento_service = ProcessoFaturamentoService()
    template_name = 'cobrancas/gerar_cob.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


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


@method_decorator(login_required, name='dispatch')
class FaturaCobrancaGeracaoContratoPlanoSaudeColetivaView(TemplateView):
    processamento_faturamento_service = ProcessoFaturamentoService()

    def get(self, request, *args, **kwargs):
        try:
            self.processamento_faturamento_service.processar_faturamento_plano_saude()
            self.processamento_faturamento_service.processar_faturas_vencidas()
            self.processamento_faturamento_service.atualizar_juros_multas_faturas_vencidas()
            return render(request, 'cobrancas/gerar_cob.html')
        except Exception as e:
            return render(request, 'cobrancas/gerar_cob.html', {'error': e})


@method_decorator(login_required, name='dispatch')
class FaturaCobrancaGeracaoContratoPlanoOdontologicoColetivaView(TemplateView):
    processamento_faturamento_service = ProcessoFaturamentoService()

    def get(self, request, *args, **kwargs):
        try:
            self.processamento_faturamento_service.processar_faturamento_plano_odontologico()
            self.processamento_faturamento_service.processar_faturas_vencidas()
            self.processamento_faturamento_service.atualizar_juros_multas_faturas_vencidas()
            return render(request, 'cobrancas/gerar_cob.html')
        except Exception as e:
            return render(request, 'cobrancas/gerar_cob.html', {'error': e})
