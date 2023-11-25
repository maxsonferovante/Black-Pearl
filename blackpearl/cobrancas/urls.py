from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from blackpearl.cobrancas.views.homeView import HomeTemplateView

urlpatterns = [
    path('relatorios/', HomeTemplateView.as_view(), name='home_cob'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)