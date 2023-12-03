from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView


from blackpearl.cobrancas.models.faturaCobrancaModels import CobrancaPlanoSaude, CobrancaPlanoOdontologico, FaturaCobranca

@method_decorator(login_required, name='dispatch')
class FaturaCobrancaListView(ListView):
    template_name = 'home_cob.html'

    context_object_name = 'list_objs'
    paginate_by = 10

    def get_queryset(self):
        cobrancas_plano_saude = CobrancaPlanoSaude.objects.all()
        cobrancas_plano_odontologico = CobrancaPlanoOdontologico.objects.all()

        todas_cobrancas = list(cobrancas_plano_saude) + list(cobrancas_plano_odontologico)

        todas_cobrancas.sort(key=lambda x: x.situacao)
        return todas_cobrancas


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FaturaCobrancaListView, self).get_context_data(**kwargs)
        context['list_obs'] = self.get_queryset()

        return context

