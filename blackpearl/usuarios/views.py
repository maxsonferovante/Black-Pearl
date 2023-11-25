from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView


class LoginCustomView(View):
    template_name = 'registration/login.html'
    success_url = 'usuarios/home_cob.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': AuthenticationForm})

    def post(self, request, *args, **kwargs):
        usuario = request.POST.get('username')
        senha = request.POST.get('password')

        user = authenticate(username=usuario, password=senha)
        if user:
            login_django(request, user)
            return render(request, self.success_url, {'user': user})
        else:
            return render(request, self.template_name, {
                'form': AuthenticationForm,
                'error': True
            })


@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = 'usuarios/home_cob.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
