
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from blackpearl.convenios import views

urlpatterns = [
    path('', views.home, name='home_conv'),
    path('cadastrar/', views.cadastrarCartao, name ='cadastrarCartao'),
    path('cadastrarFatura/', views.cadastrarFatura, name ='cadastrarFatura'),
    path('listarFaturas/', views.listarFaturas, name ='listarFaturas'),

    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
