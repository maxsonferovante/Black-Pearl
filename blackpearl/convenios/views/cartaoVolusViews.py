from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView
from blackpearl.convenios.forms.cartaoVolusForms import CartaoConvenioVolusForm, FaturaCartaoForm
from blackpearl.convenios.models.cartaoVolusModels import CartaoConvenioVolus, FaturaCartao

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
        origin = self.request.GET.get('fatura_create_origin')
        if origin == 'listagemfaturas':
            return reverse_lazy('listagemfaturas')
        else:
            cartao_pk = self.object.cartao.pk
            return reverse('cartao_visualizar', kwargs={'pk': cartao_pk})


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