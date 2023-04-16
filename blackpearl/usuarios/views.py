from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_django


# Create your views here.


# Create your views here.
def login(request):
    if request.method != 'GET':
        usuario = request.POST.get('userName')
        email = request.POST.get('email-address')
        senha = request.POST.get('password')
        user = authenticate(username=usuario,
                            email=email,
                            password=senha)
        if user:
            login_django(request, user)
            return render(request,'usuarios/home.html')
        else:
            return HttpResponse("E-mail ou senha invalidos")
    else:
        return render(request, 'usuarios/login.html')


@login_required(login_url='login')
def home(request):
    return render(request, 'usuarios/home.html')


def cadastro(request):
    if request.method == 'GET':
        return render(request, 'usuarios/cadastro.html')
    else:
        usuario = request.POST.get('userName')
        email = request.POST.get('email-address')
        senha = request.POST.get('password')

        print("{} e {}".format(email, senha))

        userName = User.objects.filter(username=usuario).first()
        if userName:
            return HttpResponse("Já exite um mano ae ")
        else:
            User.objects.create_user(username=usuario,
                                     email=email,
                                     password=senha).save()

            return render(request, 'registration/login.html')

