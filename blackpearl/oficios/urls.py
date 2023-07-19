
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from blackpearl.oficios.views import OficioListView, OficioDetailView, OficiosCreateView, OficiosUpdateView, \
    OficiosDeleteView, RenderToPdfOficioView, PdfGeneration

urlpatterns = [
    path('all/', OficioListView.as_view(), name='listar_oficios'),
    path('oficio/<int:pk>/', OficioDetailView.as_view(), name='detalhar_oficio'),
    path('oficio/add/', OficiosCreateView.as_view(), name='novo_oficio'),
    path('oficio/<int:pk>/editar/', OficiosUpdateView.as_view(), name='editar_oficio'),
    path('oficio/<int:pk>/excluir/', OficiosDeleteView.as_view(), name='excluir_oficio'),
    path('oficio/<int:pk>/pdf/', PdfGeneration.as_view(), name='exportar_oficio'),

]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Path: blackpearl\oficios\views.py