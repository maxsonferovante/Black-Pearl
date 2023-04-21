from django.contrib import admin
from django.urls import path, include

from blackpearl.associados import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('cadastrardjango/', views.cadastrardjango, name='cadastrardjango'),
    #path('consultar/', views.consultar, name='consultar'),
    #path('atualizar/', views.atualizar, name='atualizar'),
    #path('apagar/', views.apagar, name='apagar'),
]