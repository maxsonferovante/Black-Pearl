from django.shortcuts import render
from django.contrib import messages
from .forms import AssociadoForm, AssociadoModelForm
from .models import Associado

from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='login')
def home(request):
    context = {
        'associados': Associado.objects.order_by('-cpf')
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


"""
    # o formulario pode ou não ter dados, tem quando usuario usa do botão cadastar, não tem quando a pagina carrega
    formDadosPessoais = AssociadoForm(request.POST or None)


    if str(request.method) == 'POST':
        if formDadosPessoais.is_valid():
            nome = formDadosPessoais.cleaned_data['nome']
            sobrenome = formDadosPessoais.cleaned_data['sobrenome']
            email = formDadosPessoais.cleaned_data['email']

            print('{} {} e {}'.format(nome,sobrenome,email))

            messages.success(request, 'Dados cadastrados com sucesso!')
            formDadosPessoais = AssociadoForm()

        else:
            messages.error(request,'Verifique os campos preenchidos!')
    context = {
        'formDadosPessoais': formDadosPessoais

    }
    return render(request,'associados/formsdjango.html', context)
"""


@login_required(login_url='login')
def visualizar(request, associado_id):
    associado = Associado.objects.get(id=associado_id)
    context = {
        'associado': associado
    }
    return render(request, 'associados/visualizar.html', context)
