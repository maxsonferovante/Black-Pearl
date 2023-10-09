from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView
from django.views.generic import ListView


from blackpearl.convenios.models.planoOdontologicoModels import ContratoPlanoOdontologico, PlanoOdontologico, \
    DependentePlanoOdontologico
from blackpearl.convenios.models.models import TaxasAdministrativa
from blackpearl.convenios.forms.planoOdontologicoForms import ContratoPlanoOdontologicoForm, DependentePlanoOdontologicoForms
from blackpearl.associados.models import Associado


@method_decorator(login_required, name='dispatch')
class ContratoPlanoOdontologicoCreateView(CreateView):
    model = ContratoPlanoOdontologico
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
        contratante = Associado.objects.get(pk=contratante_id)
        taxa_administrativa = TaxasAdministrativa.objects.get(grupos=contratante.associacao)
        percentual_taxa = taxa_administrativa.percentual
        valor_unitario = PlanoOdontologico.objects.get(id=plano_odontologico_id).valorUnitario
        valor_total = round(((valor_unitario) / (100 - percentual_taxa)) * 100, 2)
        return JsonResponse({'valor_total': valor_total})




@method_decorator(login_required, name='dispatch')
class DependentePlanoOdontologicoCreateView(CreateView):
    model = DependentePlanoOdontologico
    form_class = DependentePlanoOdontologicoForms
    template_name = 'convenios/planoOdontologico/dependentes_contrato_plano_odont_add.html'
    success_url = reverse_lazy('listagemcontratoodontologica')

    def form_valid(self, form):
        ## verificação se a data de contratação do dependente não é anterior a data do contrato do titular
        contratoDependente = form.save(commit=False)

        if contratoDependente.dataInicio < contratoDependente.contratoTitular.dataInicio:
            form.add_error('dataInicio', 'Data de contratação não pode ser anterior a data do contrato do titular ( '+ str(contratoDependente.contratoTitular.dataInicio) +')')
            return super().form_invalid(form)

        contratoDependenteExists = DependentePlanoOdontologico.objects.filter(dependente=contratoDependente.dependente, contratoTitular=contratoDependente.contratoTitular).exists()

        if contratoDependenteExists:
            form.add_error('dependente', 'Dependente já possui um contrato ativo')
            return super().form_invalid(form)

        contratoTitular = ContratoPlanoOdontologico.objects.get(pk=contratoDependente.contratoTitular.id)
        contratoTitular.valor = contratoTitular.valor + contratoDependente.valor
        contratoTitular.save()
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class ConsultaValoresPlanoOdontologicoDependente(View):
    @csrf_exempt
    def get(self, request):
        contratoTitular = self.request.GET.get('contratoValue')

        contrato = ContratoPlanoOdontologico.objects.get(pk=contratoTitular)
        valorUnitario = contrato.planoOdontologico.valorUnitario

        percentualTaxa = TaxasAdministrativa.objects.get(grupos=contrato.contratante.associacao).percentual


        valorTotal = round(((valorUnitario) / (100 - percentualTaxa)) * 100, 2)

        return JsonResponse({
            'valorComTaxa': valorTotal,
            'valor': valorUnitario,
        })

class ConsultaDosDependentesContratoPlanoOdontologicoView(View):
    @csrf_exempt
    def get(self, request):
        contrato_id = self.request.GET.get('contratoValue')
        try:
            contrato = ContratoPlanoOdontologico.objects.get(pk=contrato_id)
            contratante = Associado.objects.get(pk=contrato.contratante.id)

            dependentes = contratante.dependentes.all()

            dependentes_data = [{'id': dep.pk, 'nomecompleto': dep.nomecompleto} for dep in dependentes]
            return JsonResponse({'has_dependents': dependentes.exists(), 'dependentes': dependentes_data})
        except Associado.DoesNotExist:
            return JsonResponse({'has_dependents': False, 'dependentes': []})

