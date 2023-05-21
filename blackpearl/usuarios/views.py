from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_django


# Create your views here.
def login(request):
    if request.method == 'POST':
        usuario = request.POST.get('userName')
        email = request.POST.get('email-address')
        senha = request.POST.get('password')
        user = authenticate(username=usuario, email=email, password=senha)
        if user:
            login_django(request, user)
            context = {
                'user' : user
            }
            return render(request, 'usuarios/home.html', context)
        else:
            return render(request, 'registration/login.html', {
                'form': AuthenticationForm,
                'error': True
            })
    else:
        return render(request, 'registration/login.html',
                      {
                          'form': AuthenticationForm
                      })


@login_required
def sair(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    return render(request, 'usuarios/home.html')


"""
def cadastro(request):
    if request.method == 'GET':
        return render(request, 'registration/cadastro.html', {
            'form': UserCreationForm
        })
    else:
        usuario = request.POST.get('userName')
        email = request.POST.get('email-address')
        senha = request.POST.get('password')

        userName = User.objects.filter(username=usuario).first()
        if userName:
          
            return render(request, 'registration/cadastro.html', {
                'form': UserCreationForm,
                "error": True
            })
        else:
           

            try:
                validate_password(password=senha, user=usuario)
                try:
                    user = User.objects.create_user(
                        username=usuario,
                        email=email,
                        password=senha
                    )
                    user.save()
                    login(request, user)
                    return render(request, 'registration/login.html')
                except ValueError:
                    return render(request, 'registration/cadastro.html', {
                        'form': UserCreationForm,
                        "error": True
                    })

            except django.contrib.auth.password_validation.ValidationError:
                return render(request, 'registration/cadastro.html', {
                    'form': UserCreationForm,
                    "error": ValueError
                })
"""

"""userName = User.objects.filter(username=usuario).first()
        if userName:
            return render(request, 'login.html', {
                    'form': UserCreationForm,
                    "error": 'Usuário já existe'
                    })
        else:
            User.objects.create_user(username=usuario,
                                     email=email,
                                     password=senha).save()

            return render(request, 'registration/login.html')
"""
