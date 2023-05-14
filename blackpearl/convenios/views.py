from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from reportlab.pdfgen import canvas

from .forms import CartaoConvenioVolusForm, FaturaCartaoForm
from .models import CartaoConvenioVolus, FaturaCartao


# Create your views here.
@login_required(login_url='login')
def home(request):
    paramentro_page = request.GET.get('page', '1')
    paramentro_limit = request.GET.get('limit', '10')

    if not (paramentro_limit.isdigit() and int(paramentro_limit) > 0):
        paramentro_limit = '10'

    cartoes =CartaoConvenioVolus.objects.filter(status__in=['ATIVO', 'SUSPENSO'])
    cartoes_paginator = Paginator(cartoes, paramentro_limit)

    try:
        page = cartoes_paginator.page(paramentro_page)
    except (EmptyPage, PageNotAnInteger):
        page = cartoes_paginator.page(1)

    context = {
        'cartoes': page
    }
    return render(request,'convenios/home.html', context)

@login_required(login_url='login')
def cadastrarCartao(request):
    if str(request.method) == 'POST':
        formCartao = CartaoConvenioVolusForm(request.POST)
        if formCartao.is_valid():
            titular = formCartao.cleaned_data['titular']

            try:
                titular_existente = CartaoConvenioVolus.objects.get(titular=titular)
                messages.warning(request,'O titular {} já tem um cartão contrado, o limite é de {}.'.format(titular, titular_existente.valorLimite))
                return render(request,'convenios/formsdjango.html', {'form': formCartao})
            except ObjectDoesNotExist:
                cartao = formCartao.save()
                messages.success(request, 'Cartão incluido com sucesso!')
                formCartao = CartaoConvenioVolusForm()
        else:
            messages.error(request, 'Verifique os campos destacados.')
    else:
        formCartao = CartaoConvenioVolusForm()
    context = {
        'form': formCartao
    }
    return render(request,'convenios/formsdjango.html', context)

@login_required(login_url='login')
def cadastrarFatura(request):
    if str(request.method) == 'POST':
        formFatura = FaturaCartaoForm(request.POST)
        if formFatura.is_valid():

            cartao = formFatura.cleaned_data['cartao']
            competencia = formFatura.cleaned_data['competencia']
            valor = formFatura.cleaned_data['valor']

            try:
                fatura_existente = FaturaCartao.objects.get(cartao=cartao,competencia=competencia)
                messages.warning(request,
                                 'O cartão do {} já tem uma fatura registrada para a competencia {}.'
                                 .format(cartao, fatura_existente.competencia))

                return render(request,'convenios/formsfatura.html', {'form': formFatura})
            except ObjectDoesNotExist:
                fatura = formFatura.save()
                messages.success(request, 'Fatura de competencia {} incluída com sucesso!'.format(fatura.competencia))
                formFatura = FaturaCartaoForm()
        else:
            messages.error(request, formFatura.errors.get('competencia'))
    else:
        formFatura = FaturaCartaoForm()
    context = {
        'form': formFatura
    }
    return render(request,'convenios/formsfatura.html', context)


def listarFaturas(request):
    paramentro_page = request.GET.get('page', '1')
    paramentro_limit = request.GET.get('limit', '10')

    if not (paramentro_limit.isdigit() and int(paramentro_limit) > 0):
        paramentro_limit = '10'

    faturas = FaturaCartao.objects.filter().order_by('competencia')
    fatura_paginator = Paginator(faturas, paramentro_limit)

    try:
        page = fatura_paginator.page(paramentro_page)
    except (EmptyPage, PageNotAnInteger):
        page = fatura_paginator.page(1)

    context = {
        'faturas': page
    }
    return render(request, 'convenios/listarFaturas.html',context)


def exporttofile(faturas, nome_arq,tipoArquivo_selecionado):

    quant_faturas = faturas.count()
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    y = 750  # Posição y inicial
    for fatura in faturas:
        if y<=50:
            pdf.showPage()
            y = 750
        # Escreve o título da fatura
        pdf.drawString(100, y, "Titular do Cartão: {}".format(fatura.cartao.titular.nomecompleto))
        y -= 20  # Move para a próxima linha
        pdf.drawString(100, y, "Empresa: {}".format(fatura.cartao.titular.empresa.nome))
        y -= 20  # Move para a próxima linha
        # Escreve as informações da fatura
        pdf.drawString(100, y, "Competência: {}".format(fatura.competencia))
        y -= 20
        pdf.drawString(100, y, "Valor da fatura: {}".format(fatura.valor))
        y -= 20
        pdf.drawString(100, y, "Valor com a taxa administrativa: {}".format(fatura.valorComTaxa))
        y -= 40  # Move duas linhas para baixo

    pdf.save()
    # Define o nome do arquivo PDF
    filename = f"{nome_arq}.pdf"
    # Envia o PDF para o navegador como um arquivo de download
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    buffer.seek(0)
    response.write(buffer.read())
    buffer.close()
    return response


def exportar(request):
    empresa_selecionada = request.GET.get('inputGroupSelectEmpresa')
    data_inicial = request.GET.get('start_date')
    data_final = request.GET.get('end_date')
    tipoArquivo_selecionado = request.GET.get('inputGroupSelectTipoArquivo')

    print(f"{empresa_selecionada}, {data_inicial}, {data_final}")

    if data_inicial and data_final and empresa_selecionada and tipoArquivo_selecionado:
        # Filtra as faturas pelo intervalo de datas e pelo nome da empresa
        if empresa_selecionada == '5':
            faturas = FaturaCartao.objects.filter(
                competencia__gte=data_inicial, competencia__lte=data_final
            ).order_by('competencia')

            nome_arq = 'faturas_{}_{}'.format(data_inicial,data_final)
        else:
            faturas = FaturaCartao.objects.filter(
                cartao__titular__empresa_id=empresa_selecionada,
                competencia__gte=data_inicial, competencia__lte=data_final
            ).order_by('competencia')
            nome_arq = 'fatura_{}_{}'.format(data_inicial,data_final)
        messages.success(request, "Dados exportados ... ")
        return exporttofile(faturas= faturas,
                            nome_arq = nome_arq,
                            tipoArquivo_selecionado=tipoArquivo_selecionado)

    return listarFaturas(request)




