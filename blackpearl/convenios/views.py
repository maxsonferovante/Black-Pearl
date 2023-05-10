from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from .forms import CartaoConvenioVolusForm
from .models import CartaoConvenioVolus

# Create your views here.
@login_required(login_url='login')
def home(request):
    cartoes = CartaoConvenioVolus.objects.all()



    context = {
        'cartoes': cartoes
    }
    return render(request,'convenios/home.html', context)

@login_required(login_url='login')
def cadastrarCartao(request):
    if str(request.method) == 'POST':
        formCartao = CartaoConvenioVolusForm(request.POST)
        if formCartao.is_valid():
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
