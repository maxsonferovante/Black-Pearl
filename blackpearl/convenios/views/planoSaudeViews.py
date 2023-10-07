from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView, View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from decimal import Decimal
import datetime

from blackpearl.convenios.models import PlanoSaude, ContratoPlanoSaude, ContratoPlanoSaudeDependente, ValoresPorFaixa, TaxasAdministrativa

from blackpearl.convenios.forms import ContratoPlanoSaudeForm, ContratoPlanoSaudeDependenteForm
from blackpearl.associados.models import Associado, Dependente


@method_decorator(login_required, name='dispatch')
class ContratoPlanoSaudeCreateView(CreateView):
    model = ContratoPlanoSaude
    form_class = ContratoPlanoSaudeForm
    template_name = 'convenios/planoSaude/contrato_plano_saude_add.html'
    success_url = reverse_lazy('listar_contratos_plano_saude')

    def form_valid(self, form):
        contrato = form.save(commit=False)
        taxa_administrativa = TaxasAdministrativa.objects.get(grupos=contrato.contratante.associacao)
        valor_faixa = ValoresPorFaixa.objects.get(pk=contrato.faixa.id)
        percentual_taxa = taxa_administrativa.percentual
        contrato.valorTotal = round((valor_faixa.valor / (100 - percentual_taxa)) * 100, 2)
        contrato.save()
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class ContratoPlanoSaudeListView(ListView):
    template_name = 'convenios/planoSaude/listagem_contratos_plano_saude.html'
    model = ContratoPlanoSaude
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

@method_decorator(login_required, name='dispatch')
class ContratoPlanoSaudeUpdateView(UpdateView):
    model = ContratoPlanoSaude
    form_class = ContratoPlanoSaudeForm
    template_name = 'convenios/planoSaude/contrato_plano_saude_add.html'
    success_url = reverse_lazy('listar_contratos_plano_saude')

@method_decorator(login_required, name='dispatch')
class ContratoPlanoSaudeDeleteView(DeleteView):
    model = ContratoPlanoSaude
    success_url = reverse_lazy('listar_contratos_plano_saude')

@method_decorator(login_required, name='dispatch')
class ContratoPlanoSaudeDetailView(DetailView):
    model = ContratoPlanoSaude
    template_name = 'convenios/planoSaude/button_model_contrato_plano_saude_detail.html'
    context_object_name = 'contrato'

@method_decorator(login_required, name='dispatch')
class ConsultaDependenteView(View):
    @csrf_exempt
    def get(self, request):
        contratante_id = self.request.GET.get('contrato')
        try:
            contratante = ContratoPlanoSaude.objects.get(pk=contratante_id)
            dependentes = contratante.contratante.dependentes.all()
            dependentes_data = [{'id': dep.pk, 'nomecompleto': dep.nomecompleto} for dep in dependentes]
            return JsonResponse({'has_dependents': dependentes.exists(), 'dependentes': dependentes_data})
        except Associado.DoesNotExist:
            return JsonResponse({'has_dependents': False, 'dependentes': []})

@method_decorator(login_required, name='dispatch')
class ConsultaValorFaixaEtaria(View):
    @csrf_exempt
    def get(self, request):
        planoSaude_id = self.request.GET.get('planoSaude_id')
        contratante_id = self.request.GET.get('contratante_id')
        atendimentoDomiciliar = self.request.GET.get('atendimentoDomiciliar')

        idade = self.calcular_idade(Associado.objects.get(pk=contratante_id).dataNascimento)

        faixa = ValoresPorFaixa.objects.filter(planoSaude_id=planoSaude_id, idadeMin__lte=idade, idadeMax__gte=idade).first()
        valorAtendimentoDomiciliar = PlanoSaude.objects.get(pk=planoSaude_id).valorAtendimentoDomiciliar
        valorAtendimentoTelefonico = PlanoSaude.objects.get(pk=planoSaude_id).valorAtendimentoTelefonico

        taxa = TaxasAdministrativa.objects.get(grupos = Associado.objects.get(pk=contratante_id).associacao)

        if atendimentoDomiciliar == 'True':
            valor = round(((faixa.valor+valorAtendimentoTelefonico) / (100-taxa.percentual)) * 100,2) + round((valorAtendimentoDomiciliar/(100-taxa.percentual)*100),2)
        else:
            valor = round(((faixa.valor+valorAtendimentoTelefonico)  / (100-taxa.percentual)) * 100,2)

        return JsonResponse({'faixa_id': faixa.id, 'valor': valor,
                             'idadeMin': faixa.idadeMin, 'idadeMax': faixa.idadeMax
                             })

    def calcular_idade(self, dataNascimento):
        data_atual = datetime.date.today()
        idade = data_atual.year - dataNascimento.year - ((data_atual.month, data_atual.day) < (dataNascimento.month, dataNascimento.day))
        return idade
@method_decorator(login_required, name='dispatch')
class ContratoPlanoSaudeDependenteCreateView(CreateView):
    model = ContratoPlanoSaudeDependente
    form_class = ContratoPlanoSaudeDependenteForm
    template_name = 'convenios/planoSaude/contrato_plano_dependente_saude_add.html'
    success_url = reverse_lazy('listar_contratos_plano_saude')

    def form_valid(self, form):

        dependente_contrato = form.save(commit=False)

        taxa_administrativa = TaxasAdministrativa.objects.get(grupos=dependente_contrato.contrato.contratante.associacao)

        valor_faixa = ValoresPorFaixa.objects.get(pk=dependente_contrato.faixa.id)

        print(valor_faixa.valor         , type(valor_faixa.valor))

        percentual_taxa = taxa_administrativa.percentual

        dependente_contrato.valorTotal = round((valor_faixa.valor / (Decimal(100) - percentual_taxa)) * 100, 2)

        dependente_contrato.save()

        titular_contrato = get_object_or_404(ContratoPlanoSaude, )
        titular_contrato.valorTotal = titular_contrato.valorTotal + dependente_contrato.valorTotal
        titular_contrato.save()

        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class ConsultaValorFaixaEtariaDependente(View):
    @csrf_exempt
    def get(self, request):
        planoSaude_id = self.request.GET.get('contrato')
        dependente_id = self.request.GET.get('dependente')
        atendimentoDomiciliar = self.request.GET.get('atendimentoDomiciliar')

        print (planoSaude_id, dependente_id, atendimentoDomiciliar)

        idade = self.calcular_idade(Dependente.objects.get(pk=dependente_id).dataNascimento)

        contrato = ContratoPlanoSaude.objects.get(pk=planoSaude_id)
        print (contrato.planoSaude_id)

        faixa = ValoresPorFaixa.objects.filter(planoSaude_id=contrato.planoSaude_id, idadeMin__lte=idade, idadeMax__gte=idade).first()

        print(idade, faixa)
        valorAtendimentoDomiciliar = PlanoSaude.objects.get(pk=contrato.planoSaude_id).valorAtendimentoDomiciliar

        valorAtendimentoTelefonico = PlanoSaude.objects.get(pk=contrato.planoSaude_id).valorAtendimentoTelefonico

        taxa = TaxasAdministrativa.objects.get(grupos = Dependente.objects.get(pk=dependente_id).titular.associacao)

        if atendimentoDomiciliar == 'True':
            valor = round(((faixa.valor+valorAtendimentoTelefonico) / (100-taxa.percentual)) * 100,2) + round((valorAtendimentoDomiciliar/(100-taxa.percentual)*100),2)
        else:
            valor = round(((faixa.valor+valorAtendimentoTelefonico)  / (100-taxa.percentual)) * 100,2)

        return JsonResponse({
                                'faixa': {
                                    'id': faixa.id,
                                    'valor': faixa.valor,
                                    'idadeMin': faixa.idadeMin,
                                    'idadeMax': faixa.idadeMax
                                },
                                'valorComTaxa': valor
                             })

    def calcular_idade(self, dataNascimento):
        data_atual = datetime.date.today()
        idade = data_atual.year - dataNascimento.year - ((data_atual.month, data_atual.day) < (dataNascimento.month, dataNascimento.day))
        return idade
