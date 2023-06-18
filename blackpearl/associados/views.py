import time
from datetime import datetime, timedelta
from io import BytesIO
from random import randint
import pandas as pd

from _decimal import Decimal

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, UpdateView, DeleteView, DetailView, CreateView, ListView
from reportlab.pdfgen import canvas
from tqdm import tqdm

from .importExcelToAssociados import import_excel_to_associado
from .forms import AssociadoModelForm, FileUploadExcelModelForm, DependenteModelForm
from .models import Associado, FileUploadExcelModel, Dependente, Empresa
from ..convenios.models import CartaoConvenioVolus, FaturaCartao


# Create your views here.
#
@method_decorator(login_required, name='dispatch')
class HomeTemplateView(ListView):
    template_name = 'associados/home.html'
    model = Associado
    paginate_by = 10
    context_object_name = 'lista_objs'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrar por nome
        nome_pesquisado = self.request.GET.get('obj')
        if nome_pesquisado:
            queryset = queryset.filter(nomecompleto__icontains=nome_pesquisado)
        else:
            queryset = queryset.all().order_by('nomecompleto')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return  context


@method_decorator(login_required, name='dispatch')
class AssociadoCreateView(CreateView):
    model = Associado
    form_class = AssociadoModelForm
    template_name_suffix = "_form"
    success_url = reverse_lazy('home_assoc')


@method_decorator(login_required, name='dispatch')
class AssociadoUpdateView(UpdateView):
    model = Associado
    form_class = AssociadoModelForm
    template_name_suffix = "_form"
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
    template_name_suffix = "_form"
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

    def get_success_url(self):
        origen = self.request.GET.get('dependente_create_origen')
        if origen == 'home_assoc':
            return reverse('home_assoc')
        else:
            associado_pk = self.object.titular.pk
            return reverse('visualizar_associado', kwargs={'pk': associado_pk})


@method_decorator(login_required, name='dispatch')
class DependenteUpdateView(UpdateView):
    model = Dependente
    form_class = DependenteModelForm
    template_name_suffix = "_form"

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
            print(arq)
            obj = FileUploadExcelModel.objects.create(
                nome="arquivo.xlsx",
                arquivo=arq
            )
            print(obj.arquivo)
            df = pd.read_excel(obj.arquivo, sheet_name='Sheet')

            total_records = len(df.index)
            progress_percent = 0

            for index in tqdm(df.index, desc='Importando dados', unit=' registro'):
                """print (df.at[index, 'Nome Completo'])
                associado = Associado(
                    nomecompleto= df.at[index, 'Nome Completo'],

                    dataNascimento='1990-01-01',

                    sexo=df.at[index, 'Sexo'],

                    cpf=str(df.at[index, 'CPF']).zfill(11),

                    identidade='',
                    orgemissor='',
                    estadocivil='S',  # ou 'C' para casado, 'D' para divorciado, 'V' para viúvo(a)

                    dataAssociacao='2022-01-01',

                    associacao='fiativo',

                    matricula=df.at[index, 'Matricula'],
                    empresa= Empresa.objects.get(nome=df.at[index, 'Departamento']),

                    email='associado@example.com',
                    dddNumeroContato='99',
                    numeroContato='999999999',
                    cep='12345-678',
                    logradouro='Rua do Associado',
                    num=123,
                    bairro='Bairro do Associado',
                    cidade='Cidade do Associado',
                    estado='PA'
                )

                associado.save()
                # Criando um CartaoConvenioVolus fictício
                cartao = CartaoConvenioVolus.objects.create(nome="Convênio Volus", titular=associado,
                                                            valorLimite=Decimal(df.at[index, 'Limite Crédito'].item()), status="ATIVO")
                cartao.save()

                # Criando uma FaturaCartao fictícia
                fatura = FaturaCartao.objects.create(cartao=cartao, valor=Decimal(df.at[index, 'Valor'].item()),
                                                     competencia=datetime.now().date())

                fatura.save()"""

                time.sleep(0.2)

                # Atualize a porcentagem de progresso
                progress_percent = int((index + 1) / total_records * 100)

            context = {
                'formUploadFile': formUploadFile,
                'progress_percent': progress_percent
            }
            return render(request, 'associados/formsdimport_excel.html', context)


            messages.success(request, 'Dados importados com sucesso!')

        else:
            messages.error(request, 'Verifique os campos destacados!')
    else:
        formUploadFile = FileUploadExcelModelForm()

    context = {
        'formUploadFile': FileUploadExcelModelForm()
    }
    return render(request, 'associados/formsdimport_excel.html', context)

@method_decorator(login_required, name='dispatch')
class ImportExcelView(View):
    def get(self, request):
        formUploadFile = FileUploadExcelModelForm()
        context = {
            'formUploadFile': formUploadFile
        }
        return render(request, 'associados/formsdimport_excel.html', context)
    def post(self,request):
        if request.method == 'POST':
            formUploadFile = FileUploadExcelModelForm(request.POST)
            if formUploadFile.is_valid():
                arq = request.FILES['files']
                print(arq)
                obj = FileUploadExcelModel.objects.create(
                    nome="arquivo.xlsx",
                    arquivo=arq
                )
                print(obj.arquivo)
                df = pd.read_excel(obj.arquivo, sheet_name='Sheet')

                total_records = len(df.index)
                progress_percent = 0

                for index in tqdm(df.index, desc='Importando dados', unit=' registro'):
                    print (df.at[index, 'Nome Completo'])
                    associado = Associado(
                        nomecompleto= df.at[index, 'Nome Completo'],

                        dataNascimento='1990-01-01',

                        sexo=df.at[index, 'Sexo'],

                        cpf=str(df.at[index, 'CPF']).zfill(11),

                        identidade='',
                        orgemissor='',
                        estadocivil='S',  # ou 'C' para casado, 'D' para divorciado, 'V' para viúvo(a)

                        dataAssociacao='2022-01-01',

                        associacao='fiativo',

                        matricula=df.at[index, 'Matricula'],
                        empresa= Empresa.objects.get(nome=df.at[index, 'Departamento']),

                        email='associado@example.com',
                        dddNumeroContato='99',
                        numeroContato='999999999',
                        cep='12345-678',
                        logradouro='Rua do Associado',
                        num=123,
                        bairro='Bairro do Associado',
                        cidade='Cidade do Associado',
                        estado='PA'
                    )

                    associado.save()
                    # Criando um CartaoConvenioVolus fictício
                    cartao = CartaoConvenioVolus.objects.create(nome="Convênio Volus", titular=associado,
                                                                valorLimite=Decimal(df.at[index, 'Limite Crédito'].item()), status="ATIVO")
                    cartao.save()

                    # Criando uma FaturaCartao fictícia
                    fatura = FaturaCartao.objects.create(cartao=cartao, valor=Decimal(df.at[index, 'Valor'].item()),
                                                         competencia=datetime.now().date())

                    fatura.save()

                    time.sleep(0.1)

                    # Atualize a porcentagem de progresso
                    progress_percent = int((index + 1) / total_records * 100)

                messages.success(request, 'Dados importados com sucesso!')

            else:
                context = {
                    'formUploadFile': formUploadFile
                }
                messages.error(request, 'Verifique os campos destacados!')
                return render(request, 'associados/formsdimport_excel.html', context)

        return render(request, 'associados/formsdimport_excel.html', {
                'formUploadFile': FileUploadExcelModelForm()
            })

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
