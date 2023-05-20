
from django.conf import settings
from django.conf.urls.static import static

import admin_kit

from django.urls import path, include, re_path
from blackpearl.convenios import views

urlpatterns = [
    path('', views.home, name='home_conv'),
    path('cadastrar/', views.cadastrarCartao, name ='cadastrarCartao'),
    path('cadastrarFatura/', views.cadastrarFatura, name ='cadastrarFatura'),
    path('listagemcartoes/', views.listagemcartoes, name ='listagemcartoes'),
    path('listarFaturas/', views.listarFaturas, name ='listarFaturas'),
    path('exportar/', views.exportar, name = 'exportar'),
    path('contratacaoodontologica/', views.contratacaoodontologica, name='contratacaoodontologica'),
    path('listarcontratacaoodontologica/', views.listarcontratacaoodontologica, name='listarcontratacaoodontologica'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += re_path(r'^admin_kit/', admin_kit.site.urls, name="admin_kit"),
