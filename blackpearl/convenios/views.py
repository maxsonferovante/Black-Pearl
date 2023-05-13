from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.contrib import messages
from .forms import CartaoConvenioVolusForm, FaturaCartaoForm
from .models import CartaoConvenioVolus, FaturaCartao

# Create your views here.
@login_required(login_url='login')
def home(request):
    cartoes =CartaoConvenioVolus.objects.filter(status__in=['ATIVO', 'SUSPENSO'])

    context = {
        'cartoes': cartoes
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
