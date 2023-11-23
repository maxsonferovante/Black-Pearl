from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView
from blackpearl.convenios.forms.cartaoVolusForms import CartaoConvenioVolusForm, FaturaCartaoForm, \
    FileUploadExcelFaturasForm
from blackpearl.convenios.models.cartaoVolusModels import CartaoConvenioVolus, FaturaCartao
from blackpearl.convenios.models.models import TaxasAdministrativa


@method_decorator(login_required, name='dispatch')
class CartaoListView(ListView):
    template_name = 'convenios/cartaoVolus/listagemcartoes.html'
    model = CartaoConvenioVolus
    paginate_by = 5
    context_object_name = 'list_objs'

    def get_queryset(self):
        queryset = super().get_queryset()
        nome_pesquisado = self.request.GET.get('obj')
        if nome_pesquisado:
            queryset = queryset.filter(titular__nomecompleto__icontains=nome_pesquisado).order_by('titular')
        else:
            queryset = queryset.all().order_by('titular')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class CartaoCreateView(CreateView):
    model = CartaoConvenioVolus
    form_class = CartaoConvenioVolusForm
    template_name = "convenios/cartaoVolus/cartaoconveniovolus_criar_form.html"
    success_url = reverse_lazy('listagemcartoes')

    def form_valid(self, form):
        cartao = form.save(commit=False)
        if ( cartao.valorLimite <=0):
            form.add_error('valorLimite', 'Valor do Limite deve ser maior que zero!')
            return self.form_invalid(form)
        cartao.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class CartaoUpdateView(UpdateView):
    model = CartaoConvenioVolus
    form_class = CartaoConvenioVolusForm
    template_name = "convenios/cartaoVolus/cartaoconveniovolus_criar_form.html"
    success_url = reverse_lazy('listagemcartoes')


@method_decorator(login_required, name='dispatch')
class CartaoDetailView(DetailView):
    template_name = 'convenios/cartaoVolus/cartao_detalhes.html'
    model = CartaoConvenioVolus

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cartao_pk = self.kwargs['pk']
        cartao = CartaoConvenioVolus.objects.get(pk=cartao_pk)
        context['cartao'] = cartao
        return context


@method_decorator(login_required, name='dispatch')
class CartaoDeleteView(DeleteView):
    model = CartaoConvenioVolus
    success_url = reverse_lazy('listagemcartoes')


@method_decorator(login_required, name='dispatch')
class FaturaCreateView(CreateView):
    model = FaturaCartao
    form_class = FaturaCartaoForm

    template_name = "convenios/cartaoVolus/faturacartao_criar_form.html"

    def get_success_url(self):
        # Verifica a origem da solicitação na sessão
        origin = self.request.GET.get('origin', None)
        if origin == 'cartaodetalhes':
            cartao_pk = self.object.cartao.pk
            return reverse('cartao_visualizar', kwargs={'pk': cartao_pk})
        else:
            return reverse_lazy('listagemfaturas')

    def form_valid(self, form):
        fatura = form.save(commit=False)
        if ( fatura.valor > fatura.cartao.valorLimite ):
            form.add_error('valor', 'Valor da Fatura maior que o limite do cartão')
            return self.form_invalid(form)

        if ( fatura.valor < 0 ):
            form.add_error('valor', 'Valor da Fatura não pode ser negativo')
            return self.form_invalid(form)
        faturaExisteNaMesmaCompetencia = FaturaCartao.objects.filter(cartao=fatura.cartao,
                                                                     competencia__year=fatura.competencia.year,
                                                                     competencia__month=fatura.competencia.month).exists()
        if ( faturaExisteNaMesmaCompetencia ):
            form.add_error('competencia', 'Já existe uma fatura para esse cartão nessa competência')
            return self.form_invalid(form)

        fatura.save()
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class FaturaDeleteView(DeleteView):
    model = FaturaCartao
    success_url = reverse_lazy('listagemfaturas')


@method_decorator(login_required, name='dispatch')
class FaturaUpdateView(UpdateView):
    model = FaturaCartao
    form_class = FaturaCartaoForm
    template_name_suffix = "_criar_form"
    success_url = reverse_lazy('listagemfaturas')


@method_decorator(login_required, name='dispatch')
class FaturaListView(ListView):
    template_name = 'convenios/cartaoVolus/listagem_faturas.html'
    model = FaturaCartao
    context_object_name = 'list_objs'
    paginate_by = 5
    def get_queryset(self):
        queryset = super().get_queryset()
        nome_pesquisado = self.request.GET.get('obj')
        if nome_pesquisado:
            queryset = queryset.filter(cartao__titular__nomecompleto__icontains=nome_pesquisado).order_by('cartao')
        else:
            queryset = queryset.all().order_by('cartao')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class ConsultaTaxaView(View):
    @csrf_exempt
    def get(self, request):
        valor = self.request.GET.get('valor')
        try:
            taxa_administrativa = TaxasAdministrativa.objects.get(grupos='outros')
            percentual_taxa = taxa_administrativa.percentual
            taxa = 1 + (percentual_taxa / Decimal(100.0))
            valorTaxa = round(Decimal(valor) * taxa, 2)
            return JsonResponse({'valorTaxa': valorTaxa})
        except:
            return JsonResponse({'valorTaxa': 0})


@method_decorator(login_required, name='dispatch')
class ImportarFaturasView(View):
    template_name = "convenios/cartaoVolus/formsdimport_excel.html"
    form_class = FileUploadExcelFaturasForm()
    success_url = reverse_lazy('listagemfaturas')
    def get(self, request, *args, **kwargs):
        context = {
            'formUploadFileFaturas': self.form_class,
        }
        return render(request, self.template_name, context)
