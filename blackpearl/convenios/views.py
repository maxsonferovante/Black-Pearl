from io import BytesIO
import openpyxl

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib import messages
from reportlab.pdfgen import canvas

from .forms import CartaoConvenioVolusForm, FaturaCartaoForm
from .models import CartaoConvenioVolus, FaturaCartao


# Create your views here.
@login_required(login_url='login')
def home(request):
    nome_pesquisado = request.GET.get('obj')
    if nome_pesquisado:
        cartoes = CartaoConvenioVolus.objects.filter(titular__nomecompleto__icontains=nome_pesquisado).order_by(
            'titular')
    else:
        cartoes = CartaoConvenioVolus.objects.all()

    paramentro_page = request.GET.get('page', '1')
    paramentro_limit = request.GET.get('limit', '10')

    if not (paramentro_limit.isdigit() and int(paramentro_limit) > 0):
        paramentro_limit = '10'

    cartoes_paginator = Paginator(cartoes, paramentro_limit)

    try:
        page = cartoes_paginator.page(paramentro_page)
    except (EmptyPage, PageNotAnInteger):
        page = cartoes_paginator.page(1)

    context = {
        'list_objs': page
    }
    return render(request, 'convenios/home.html', context)


@login_required(login_url='login')
def cadastrarCartao(request):

    if str(request.method) == 'POST':
        formCartao = CartaoConvenioVolusForm(request.POST)
        if formCartao.is_valid():
            titular = formCartao.cleaned_data['titular']

            try:
                titular_existente = CartaoConvenioVolus.objects.get(titular=titular)
                messages.warning(request, 'O titular {} já tem um cartão contrado, o limite é de {}.'.format(titular,
                                                                                                             titular_existente.valorLimite))
                return render(request, 'convenios/formsdjango.html', {'form': formCartao})
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
    return render(request, 'convenios/formsdjango.html', context)


@login_required(login_url='login')
def cadastrarFatura(request):
    if str(request.method) == 'POST':
        formFatura = FaturaCartaoForm(request.POST)
        if formFatura.is_valid():

            cartao = formFatura.cleaned_data['cartao']
            competencia = formFatura.cleaned_data['competencia']
            valor = formFatura.cleaned_data['valor']

            try:
                fatura_existente = FaturaCartao.objects.get(cartao=cartao, competencia=competencia)
                messages.warning(request,
                                 'O cartão do {} já tem uma fatura registrada para a competencia {}.'
                                 .format(cartao, fatura_existente.competencia))

                return render(request, 'convenios/formsfatura.html', {'form': formFatura})
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
    return render(request, 'convenios/formsfatura.html', context)


def listarFaturas(request):
    nome_pesquisado = request.GET.get('obj')
    if nome_pesquisado:
        faturas = FaturaCartao.objects.filter(cartao__titular__nomecompleto__icontains=nome_pesquisado).order_by(
            'cartao')
    else:
        faturas = FaturaCartao.objects.filter().order_by('competencia')

    paramentro_page = request.GET.get('page', '1')
    paramentro_limit = request.GET.get('limit', '10')

    if not (paramentro_limit.isdigit() and int(paramentro_limit) > 0):
        paramentro_limit = '10'

    fatura_paginator = Paginator(faturas, paramentro_limit)

    try:
        page = fatura_paginator.page(paramentro_page)
    except (EmptyPage, PageNotAnInteger):
        page = fatura_paginator.page(1)

    context = {
        'list_objs': page
    }
    return render(request, 'convenios/listarFaturas.html', context)


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

            nome_arq = 'faturas_{}_{}'.format(data_inicial, data_final)
        else:
            faturas = FaturaCartao.objects.filter(
                cartao__titular__empresa_id=empresa_selecionada,
                competencia__gte=data_inicial, competencia__lte=data_final
            ).order_by('competencia')
            nome_arq = 'fatura_{}_{}'.format(data_inicial, data_final)

        return exporttofile(faturas=faturas,
                            nome_arq=nome_arq,
                            tipoArquivo_selecionado=tipoArquivo_selecionado)

    return listarFaturas(request)


def exporttofile(faturas, nome_arq, tipoArquivo_selecionado):
    filename = f"{nome_arq}"

    if tipoArquivo_selecionado == '1':
        quant_faturas = faturas.count()
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        y = 750  # Posição y inicial
        for fatura in faturas:
            if y <= 50:
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
        filename = filename + ".pdf"
        # Envia o PDF para o navegador como um arquivo de download
        response = HttpResponse(content_type='application/pdf')

        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        buffer.seek(0)

        response.write(buffer.read())

        buffer.close()
    elif tipoArquivo_selecionado == '2':
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = nome_arq
        # Escreve os dados da lista de faturas na planilha
        ws['A1'] = "Titular"
        ws['B1'] = "Empresa"
        ws['C1'] = "Competêcia"
        ws['D1'] = "Valor"
        ws['E1'] = "Valor com taxa"

        for i, fatura in enumerate(faturas):
            ws.cell(row=i + 2, column=1, value=fatura.cartao.titular.nomecompleto)
            ws.cell(row=i + 2, column=2, value=fatura.cartao.titular.empresa.nome)
            ws.cell(row=i + 2, column=3, value=fatura.competencia)
            ws.cell(row=i + 2, column=4, value=fatura.valor)
            ws.cell(row=i + 2, column=5, value=fatura.valorComTaxa)

        # Cria uma resposta HTTP com o arquivo XLSX
        response = HttpResponse(content_type='application/xlsx')
        response['Content-Disposition'] = f'attachment; filename={nome_arq}.xlsx'
        wb.save(response)


    elif tipoArquivo_selecionado == '3':
        faturas_txt = ''
        for fatura in faturas:
            matricula = str(fatura.cartao.titular.matricula).zfill(6)
            valorComTaxa = str(fatura.valorComTaxa)[:4].replace('.', '').zfill(12)
            faturas_txt += '{} {}\n'.format(matricula, valorComTaxa)

        response = HttpResponse(faturas_txt, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{nome_arq}.txt'

    return response
