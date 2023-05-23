from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from blackpearl.convenios.views import HomeTemplateView, CartaoListView, CartaoCreateView

from blackpearl.convenios import views
urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home_conv'),
    path('cadastrarcartao/', CartaoCreateView.as_view(), name ='cartao_cadastrar'),
    path('cadastrarFatura/', views.cadastrarFatura, name ='cadastrarFatura'),
    path('listagemcartoes/', CartaoListView.as_view(), name ='listagemcartoes'),
    path('listarFaturas/', views.listarFaturas, name ='listarFaturas'),
    path('exportar/', views.exportar, name = 'exportar'),
    path('contratacaoodontologica/', views.contratacaoodontologica, name='contratacaoodontologica'),
    path('listarcontratacaoodontologica/', views.listarcontratacaoodontologica, name='listarcontratacaoodontologica'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)