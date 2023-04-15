from django.urls import path

from blackpearl.usuarios import views

urlpatterns = [
    path('',views.login, name='login'),
    path('cadastro/',views.cadastro, name='cadastro'),
    path('home/', views.plataforma, name ='home')
]

