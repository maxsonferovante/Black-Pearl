from datetime import datetime, timedelta
from io import BytesIO
from random import randint

from _decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from faker import Faker
from reportlab.pdfgen import canvas

from .importExcelToAssociados import import_excel_to_associado
from .forms import AssociadoModelForm, FileUploadExcelModelForm, DependenteModelForm
from .models import Associado, FileUploadExcelModel, Dependente, Empresa
from ..convenios.models import CartaoConvenioVolus, FaturaCartao


# Create your views here.

@login_required(login_url='login')
def home(request):
    nome_pesquisa = request.GET.get('obj')
    if nome_pesquisa:
        associados = Associado.objects.filter(nomecompleto__icontains=nome_pesquisa).order_by('nomecompleto')
    else:
        associados = Associado.objects.all().order_by('nomecompleto')

    paramentro_page = request.GET.get('page', '1')
    paramentro_limit = request.GET.get('limit', '10')

    if not (paramentro_limit.isdigit() and int(paramentro_limit) > 0):
        paramentro_limit = '10'

    associados_paginator = Paginator(associados, paramentro_limit)
    try:
        page = associados_paginator.page(paramentro_page)
    except (EmptyPage, PageNotAnInteger):
        page = associados_paginator.page(1)

    ##gerador_dados(5)
    context = {
        'list_objs': page

    }
    return render(request, 'associados/home.html', context)


@login_required(login_url='login')
def cadastrardjango(request):
    # o formulario pode ou não ter dados, tem quando usuario usa do botão cadastar, não tem quando a pagina carrega

    if str(request.method) == 'POST':
        formDadosAsssociado = AssociadoModelForm(request.POST)
        if formDadosAsssociado.is_valid():
            nomecompleto = formDadosAsssociado.cleaned_data['nomecompleto']
            cpf = formDadosAsssociado.cleaned_data['cpf']
            try:
                associado_existente = Associado.objects.get(nomecompleto=nomecompleto, cpf=cpf)
                messages.warning(request, f'O associado "{nomecompleto}" já está cadastrado.')
                return render(request, 'associados/formsdjango.html', {'form': formDadosAsssociado})
            except ObjectDoesNotExist:

                assoc = formDadosAsssociado.save()
                messages.success(request, f'Dados de {assoc.nomecompleto} cadastrados com sucesso!')
                formDadosAsssociado = AssociadoModelForm()
        else:
            messages.error(request, 'Verifique os campos destacados.')
    else:
        formDadosAsssociado = AssociadoModelForm()
    context = {
        'form': formDadosAsssociado
    }
    return render(request, 'associados/formsdjango.html', context)


@login_required(login_url='login')
def cadastrardependentes(request):
    # o formulario pode ou não ter dados, tem quando usuario usa do botão cadastar, não tem quando a pagina carrega

    if str(request.method) == 'POST':
        form = DependenteModelForm(request.POST)
        if form.is_valid():
            nomecompleto = form.cleaned_data['nomecompleto']
            cpf = form.cleaned_data['cpf']

            try:
                associado_existente = Dependente.objects.get(nomecompleto=nomecompleto, cpf=cpf)
                messages.warning(request, f'O dependente "{nomecompleto}" já está cadastrado.')
                return render(request, 'associados/forms_dependente.html', {'form': form})
            except ObjectDoesNotExist:
                depent = form.save()
                messages.success(request, f'Dados de {depent.nomecompleto} cadastrados com sucesso!')
                form = DependenteModelForm()

        else:
            messages.error(request, 'Verifique os campos destacados.')

    else:
        form = DependenteModelForm()
    context = {
        'form': form
    }
    return render(request, 'associados/forms_dependente.html', context)


@login_required(login_url='login')
def visualizar(request, associado_id):
    associado = Associado.objects.get(pk=associado_id)

    dependentes = associado.dependentes.all()
    context = {
        'dependentes': dependentes

    }
    return render(request, 'associados/home.html', context)


@login_required(login_url='login')
def editar(request, associado_id):
    if request.method == 'POST':
        associado = Associado.objects.get(pk=associado_id)
        formAssociado = AssociadoModelForm(request.POST, instance=associado)
        print(associado_id, associado, request.method)
        if formAssociado.is_valid():
            formAssociado.save()
            return redirect('home_assoc')
        else:
            print(formAssociado.errors)
    else:
        associado = Associado.objects.get(id=associado_id)
        formAssociado = AssociadoModelForm(
            instance=associado
        )
    return render(request, 'associados/editar.html', {
        'form': formAssociado
    })
@login_required(login_url='login')
def excluir(request, associado_id):
    if request.method == 'POST':
        associado = Associado.objects.get(pk=associado_id)
        associado.delete()

    return HttpResponseRedirect(reverse('home_assoc'))


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
            valorLimite=quant*10,
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


