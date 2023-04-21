from django.contrib import admin
from django.urls import path, include

from blackpearl.associados import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastrar/', views.cadastrardjango, name='cadastrar'),

    #path('consultar/', views.consultar, name='consultar'),
    #path('atualizar/', views.atualizar, name='atualizar'),
    #path('apagar/', views.apagar, name='apagar'),
]
