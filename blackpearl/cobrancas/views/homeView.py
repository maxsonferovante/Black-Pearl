from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from blackpearl.cobrancas.models.faturaCobrancaModels import CobrancaPlanoSaude, CobrancaPlanoOdontologico, FaturaCobranca


@method_decorator(login_required, name='dispatch')
class FaturaCobrancaListView(ListView):
    template_name = 'home_cob.html'
    model = FaturaCobranca
    context_object_name = 'list_objs'
    paginate_by = 10


