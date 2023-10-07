from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView
from django.views.generic import ListView


from blackpearl.convenios.models.planoOdontologicoModels import ContratoPlanoOdontologico, PlanoOdontologico
from blackpearl.convenios.models.models import TaxasAdministrativa
from blackpearl.convenios.forms.planoOdontologicoForms import ContratoPlanoOdontologicoForm
from blackpearl.associados.models import Associado


@method_decorator(login_required, name='dispatch')
class ContratoPlanoOdontologicoCreateView(CreateView):
    form_class = ContratoPlanoOdontologicoForm
    template_name = 'convenios/planoOdontologico/contratacaoplanoodontologico_criar_form.html'
    success_url = reverse_lazy('listagemcontratoodontologica')



@method_decorator(login_required, name='dispatch')
class ContratoPlanoOdontologicoDetailView(DetailView):
    model = ContratoPlanoOdontologico
    template_name = 'convenios/planoOdontologico/contratoplanoOdontologico_detalhes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contrato_pk = self.kwargs['pk']
        contrato = ContratoPlanoOdontologico.objects.get(pk=contrato_pk)
        context['contrato'] = contrato
        return context



@method_decorator(login_required, name='dispatch')
class ContratoPlanoOdontologicoUpdateView(UpdateView):
    model = ContratoPlanoOdontologico
    form_class = ContratoPlanoOdontologicoForm
    template_name = 'convenios/planoOdontologico/contratacaoplanoodontologico_criar_form.html'
    success_url = reverse_lazy('listagemcontratoodontologica')


@method_decorator(login_required, name='dispatch')
class ContratoPlanoOdontologicoDeleteView(DeleteView):
    model = ContratoPlanoOdontologico
    success_url = reverse_lazy('listagemcontratoodontologica')


@method_decorator(login_required, name='dispatch')
class ContratoOdontologicaListView(ListView):
    template_name = 'convenios/planoOdontologico/listagem_contratacaoodontologica.html'
    model = ContratoPlanoOdontologico
    context_object_name = 'list_objs'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        nome_pesquisado = self.request.GET.get('obj')
        if nome_pesquisado:
            queryset = queryset.filter(contratante__nomecompleto__icontains=nome_pesquisado).order_by('contratante')
        else:
            queryset = queryset.order_by('contratante')
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class VerificarAssociacaoView(View):
    @csrf_exempt
    def get(self, request):
        contratante_id = self.request.GET.get('contratante_id')
        plano_odontologico_id = self.request.GET.get('plano_odontologico_id')
        quantidade_dependentes = self.request.GET.get('quantidade_dependentes')

        print(contratante_id, plano_odontologico_id, quantidade_dependentes)

        contratante = Associado.objects.get(pk=contratante_id)
        taxa_administrativa = TaxasAdministrativa.objects.get(grupos=contratante.associacao)
        percentual_taxa = taxa_administrativa.percentual

        valor_unitario = PlanoOdontologico.objects.get(id=plano_odontologico_id).valorUnitario


        # instance.valor = (valorPlano / (Decimal(100.0) - taxa.percentual)) * Decimal(100.0)
        valor_total = round(((valor_unitario + quantidade_dependentes + 1) / (100 - percentual_taxa)) * 100, 2)

        print(valor_unitario, percentual_taxa, valor_total)

        return JsonResponse({'valor_total': valor_total})


class VerificarDependentesView(View):
    @csrf_exempt
    def get(self, request):
        contratante_id = self.request.GET.get('contratante_id')
        contratante_id = request.GET.get('contratante_id')
        try:
            contratante = Associado.objects.get(pk=contratante_id)
            dependentes = contratante.dependentes.all()
            dependentes_data = [{'id': dep.pk, 'nomecompleto': dep.nomecompleto} for dep in dependentes]
            return JsonResponse({'has_dependents': dependentes.exists(), 'dependentes': dependentes_data})
        except Associado.DoesNotExist:
            return JsonResponse({'has_dependents': False, 'dependentes': []})

