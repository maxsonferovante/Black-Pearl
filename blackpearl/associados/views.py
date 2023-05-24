from datetime import datetime, timedelta
from io import BytesIO
from random import randint

from _decimal import Decimal

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, UpdateView, DeleteView, DetailView, CreateView, ListView
from reportlab.pdfgen import canvas

from .importExcelToAssociados import import_excel_to_associado
from .forms import AssociadoModelForm, FileUploadExcelModelForm, DependenteModelForm
from .models import Associado, FileUploadExcelModel, Dependente, Empresa
from ..convenios.models import CartaoConvenioVolus, FaturaCartao


# Create your views here.
#
@method_decorator(login_required, name='dispatch')
class HomeTemplateView(ListView):
    template_name = 'associados/home.html'


    def get_context_data(self, **kwargs):
        context = super(HomeTemplateView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        nome_pesquisa = self.request.GET.get('obj')
        if nome_pesquisa:
            associados = Associado.objects.filter(nomecompleto__icontains=nome_pesquisa).order_by('nomecompleto')
        else:
            associados = Associado.objects.all().order_by('nomecompleto')

        paramentro_page = self.request.GET.get('page', '1')
        paramentro_limit = self.request.GET.get('limit', '10')

        if not (paramentro_limit.isdigit() and int(paramentro_limit) > 0):
            paramentro_limit = '10'

        associados_paginator = Paginator(associados, paramentro_limit)
        try:
            page = associados_paginator.page(paramentro_page)
        except (EmptyPage, PageNotAnInteger):
            page = associados_paginator.page(1)

        ##gerador_dados(5)
        return render(request, self.template_name, {
            'object_list': page
        })


@method_decorator(login_required, name='dispatch')
class AssociadoCreateView(CreateView):
    model = Associado
    form_class = AssociadoModelForm
    template_name_suffix = "_criar_form"
    success_url = reverse_lazy('home_assoc')


@method_decorator(login_required, name='dispatch')
class AssociadoUpdateView(UpdateView):
    model = Associado
    form_class = AssociadoModelForm
    template_name_suffix = "_editar_form"
    success_url = reverse_lazy('home_assoc')


@method_decorator(login_required, name='dispatch')
class AssociadoDetailView(DetailView):
    template_name = 'associados/associado_detalhes.html'
    model = Associado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        associado_pk = self.kwargs['pk']  # Captura o parâmetro 'associado_pk' da URL
        associado = Associado.objects.get(pk=associado_pk)
        context['associado'] = associado
        return context


@method_decorator(login_required, name='dispatch')
class AssociadoDeleteView(DeleteView):
    model = Associado
    success_url = reverse_lazy('home_assoc')


@method_decorator(login_required, name='dispatch')
class DependenteCreateView(SuccessMessageMixin, CreateView):
    model = Dependente
    form_class = DependenteModelForm
    template_name_suffix = "_criar_form"
    success_url = reverse_lazy('home_assoc')

    def form_valid(self, form):
        # Verificar a validação do formulário personalizado
        if form.is_valid():
            # Executar a validação padrão do CreateView
            response = super().form_valid(form)
            # Redirecionar para a página de sucesso
            return response
        else:
            return self.render_to_response(self.get_context_data(form=form))


@method_decorator(login_required, name='dispatch')
class DependenteUpdateView(UpdateView):
    model = Dependente
    form_class = DependenteModelForm
    template_name_suffix = "_editar_form"

    def get_success_url(self):
        associado_pk = self.object.titular.pk
        return reverse('visualizar_associado', kwargs={'pk': associado_pk})


@method_decorator(login_required, name='dispatch')
class DependenteDeleteView(DeleteView):
    model = Dependente

    def get_success_url(self):
        associado_pk = self.object.titular.pk
        return reverse('visualizar_associado', kwargs={'pk': associado_pk})


@login_required(login_url='login')
def importExcel(request):
    if request.method == 'POST':
        formUploadFile = FileUploadExcelModelForm(request.POST)
        if formUploadFile.is_valid():
            arq = request.FILES['files']
            obj = FileUploadExcelModel.objects.create(
                nome="teste",
                arquivo=arq
            )
            ## modulo importExcelToAssociado.py responsável pela migração dos dados
            import_excel_to_associado(obj)
            obj = FileUploadExcelModel.objects.get(arquivo=obj.arquivo)

            obj.delete()

            formUploadFile = FileUploadExcelModelForm()

            messages.success(request, 'Dados importados com sucesso!')

        else:
            messages.error(request, 'Verifique os campos destacados!')
    else:
        formUploadFile = FileUploadExcelModelForm()

    context = {
        'formUploadFile': formUploadFile
    }
    return render(request, 'associados/formsdimport_excel.html', context)


def export_pdf(request, assoc_id):
    assoc = Associado.objects.get(id=assoc_id)

    buffer = BytesIO()

    p = canvas.Canvas(buffer)
    p.drawString(100, 750, "{} {}".format(assoc.nome, assoc.sobrenome))

    p.drawString(100, 730, "{} {}".format(assoc.dataNascimento, assoc.cpf))

    p.drawString(100, 710, "{()} {} - {}", assoc.dddNumeroContato, assoc.numeroContato, assoc.email)

    p.drawString(100, 690, "CEP: {} Logradouro: {} N: {}".format(assoc.cep, assoc.logradouro, assoc.num))

    p.drawString(100, 690, "Bairro: {} Cidade: {} Estado(UF): {}".format(assoc.bairro, assoc.cidade, assoc.estado))

    p.showPage()
    p.save()

    # Define o nome do arquivo PDF
    filename = f"cadastro_{assoc.id}.pdf"

    # Envia o PDF para o navegador como um arquivo de download
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    buffer.seek(0)
    response.write(buffer.read())
    buffer.close()
    return response


def gerador_dados(quant):
    for i in range(quant):
        # Cria um objeto Associado com os dados gerados
        associado = Associado(
            nomecompleto="vinicius almeida campos",
            dataNascimento="1999-05-29",
            sexo="M",
            cpf="12312312323",
            identidade="4764825",
            orgemissor="SSP",
            estadocivil="S",
            dataAssociacao="2019-04-01",
            associacao="Agredado(a)",
            matricula=randint(1, 1500),
            empresa=Empresa.objects.get(nome="SINDIPORTO"),
            email="vidalok@gmail.com",
            dddNumeroContato="91 982299627",
            numeroContato="982299627",
            cep="66650550",
            logradouro="PASSAGEM COMERCIÁRIOS",
            num=3,
            bairro="COQUEIRO",
            cidade="BELÉM",
            estado="PA",
        )

        # Salva o objeto no banco de dados
        associado.save()
        cartao = CartaoConvenioVolus(
            nome='Convênio Volus',
            titular=associado,
            valorLimite=quant * 10,
            status='ATIVO',
        )
        cartao.save()
        valor = Decimal(randint(300, 1500))  # gerar um valor aleatório entre 500 e 1500
        taxa_adm = valor * Decimal('0.05')  # taxa de administração de 5%
        valor_com_taxa = valor + taxa_adm
        competencia = datetime.now().date() - timedelta(days=30 * i)  # gerar a data de competência retroativamente

        # criar a fatura
        fatura = FaturaCartao(
            cartao=cartao,
            valor=valor,
            valorComTaxa=valor_com_taxa,
            competencia=competencia,
        )
        fatura.save()
