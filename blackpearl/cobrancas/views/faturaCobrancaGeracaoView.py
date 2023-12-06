from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView

from blackpearl.cobrancas.models.faturaCobrancaModels import CobrancaPlanoSaude, CobrancaPlanoOdontologico
from blackpearl.cobrancas.forms.faturaCobrancaGeracaoForm import FaturaCobrancaGeracaoContratoPlanoSaudeForm, \
    FaturaCobrancaGeracaoContratoPlanoOdontologicoForm

from blackpearl.cobrancas.services.processoFaturamentoService import ProcessoFaturamentoService
from blackpearl.convenios.models.planoOdontologicoModels import ContratoPlanoOdontologico
from blackpearl.convenios.models.planoSaudeModels import ContratoPlanoSaude


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

    def form_valid(self, form):
        contratoPlanoSaude = form.save(commit=False)

        contratoPlanoSaudeExiste = CobrancaPlanoSaude.objects.filter(
            contratoPlanoSaude=contratoPlanoSaude.contratoPlanoSaude,
            situacao=contratoPlanoSaude.situacao,
            dataDoVencimento=contratoPlanoSaude.dataDoVencimento
        ).exists()

        if contratoPlanoSaudeExiste:
            form.add_error('contratoPlanoSaude', 'Já existe uma cobrança para este contrato com esta situação e data de vencimento')
            return super().form_invalid(form)

        contratoPlanoSaude.valotPago = 0
        contratoPlanoSaude.juros = 0
        contratoPlanoSaude.multa = 0
        contratoPlanoSaude.dataDoPagamento = None
        contratoPlanoSaude.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class FaturaCobrancaGeracaoContratoPlanoOdontologicoCreateView(CreateView):
    model = CobrancaPlanoOdontologico
    form_class = FaturaCobrancaGeracaoContratoPlanoOdontologicoForm
    template_name = 'cobrancas/gerar_cob_planoodontologico_contrato.html'
    success_url = reverse_lazy('home_cob')

    def form_valid(self, form):
        contratoPlanoOdontologico = form.save(commit=False)

        contratoPlanoOdontologicoExiste = CobrancaPlanoOdontologico.objects.filter(
            contratoPlanoOdontologico=contratoPlanoOdontologico.contratoPlanoOdontologico,
            situacao=contratoPlanoOdontologico.situacao,
            dataDoVencimento=contratoPlanoOdontologico.dataDoVencimento
        ).exists()

        if contratoPlanoOdontologicoExiste:
            form.add_error('contratoPlanoOdontologico', 'Já existe uma cobrança para este contrato com esta situação e data de vencimento')
            return super().form_invalid(form)

        contratoPlanoOdontologico.valotPago = 0
        contratoPlanoOdontologico.juros = 0
        contratoPlanoOdontologico.multa = 0
        contratoPlanoOdontologico.dataDoPagamento = None
        contratoPlanoOdontologico.save()
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class FaturaCobrancaGeracaoConsultaValorContratoIndividualView(TemplateView):

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        contratoPlanoSaude = request.GET.get('contratoPlanoSaude')
        try:
            valorContratadoPlanoSaude = ContratoPlanoSaude.objects.get(pk=contratoPlanoSaude).valorTotal
            print(valorContratadoPlanoSaude, "valorContratadoPlanoSaude")
            return JsonResponse({'valorContratado': valorContratadoPlanoSaude})
        except ContratoPlanoSaude.DoesNotExist:
            try:
                valorContratadoPlanoOdontologico = ContratoPlanoOdontologico.objects.get(pk=contratoPlanoSaude).valor
                print(valorContratadoPlanoOdontologico, "valorContratadoPlanoOdontologico")
                return JsonResponse({'valorContratado': valorContratadoPlanoOdontologico})
            except ContratoPlanoOdontologico.DoesNotExist:
                return JsonResponse({'error': 'Contrato não encontrado'})
            except Exception as e:
                return JsonResponse({'error': e})


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
