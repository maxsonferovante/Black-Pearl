from django.urls import path, include

from blackpearl.usuarios import views

urlpatterns = [
    path('', views.login, name='login'),
    #path('create_login/', views.cadastro, name='cadastro'),
    path('home/', views.home, name='home'),


]
