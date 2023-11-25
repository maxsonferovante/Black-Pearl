from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from blackpearl.convenios.models.planoSaudeModels import ContratoPlanoSaude, ContratoPlanoSaudeDependente
from blackpearl.cobrancas.services.relatoriosConvenios import RelatoriosConvenios




@method_decorator(login_required, name='dispatch')
class HomeTemplateView(TemplateView):
    template_name = 'home_cob.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        relatorios = RelatoriosConvenios(ContratoPlanoSaude)

        context['ativos_e_inativos'] = relatorios.ativosEInativos()
        context['total_por_associacao'] = relatorios.totalPorAssociacao()

        return context