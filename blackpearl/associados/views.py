from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages
from tablib import Dataset
from blackpearl.settings import BASE_DIR
from .forms import AssociadoModelForm, FileUploadExcelModelForm
from .models import Associado, FileUploadExcelModel

from django.contrib.auth.decorators import login_required

import pandas as pd

from .importExcelToAssociados import import_excel_to_associado
# Create your views here.

@login_required(login_url='login')
def home(request):
    associados = Associado.objects.all()
    context = {
        'associados': associados,

    }
    return render(request, 'associados/home.html', context)


@login_required(login_url='login')
def cadastrardjango(request):
    # o formulario pode ou não ter dados, tem quando usuario usa do botão cadastar, não tem quando a pagina carrega

    if str(request.method) == 'POST':
        formDadosAsssociado = AssociadoModelForm(request.POST)
        if formDadosAsssociado.is_valid():

            assoc = formDadosAsssociado.save()
            messages.success(request, 'Dados de {} {} cadastrados com sucesso!'.format(assoc.nome, assoc.sobrenome))

            formDadosAsssociado = AssociadoModelForm()

        else:
            messages.error(request, 'Verifique os campos destacados.')

    else:
        formDadosAsssociado = AssociadoModelForm()
    context = {
        'formDadosAssociado': formDadosAsssociado
    }
    return render(request, 'associados/formsdjango.html', context)


@login_required(login_url='login')
def visualizar(request, associado_id):
    associado = Associado.objects.get(pk=associado_id)

    context = {
        'associado': associado
    }
    return HttpResponseRedirect(reverse(
        'home'
    ))
    # return render(request, 'associados/editar.html', context)


@login_required(login_url='login')
def editar(request, associado_id):
    if request.method == 'POST':
        associado = Associado.objects.get(pk=associado_id)
        formAssociado = AssociadoModelForm(request.POST, instance=associado)
        if formAssociado.is_valid():
            assoc = formAssociado.save()

            messages.success(request, 'Dados de {} {} cadastrados com sucesso!'.format(assoc.nome, assoc.sobrenome))
            return render(request, 'associados/editar.html', {
                'form': formAssociado
            })
    else:
        associado = Associado.objects.get(pk=associado_id)
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
    return HttpResponseRedirect(reverse('home'))


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
            messages.error(request,'Verifique os campos destacados!')
    else:
        formUploadFile = FileUploadExcelModelForm()

    context = {
            'formUploadFile': formUploadFile
        }
    return render(request, 'associados/formsdimport_excel.html', context)
