from django.urls import path
from blackpearl.usuarios.views import HomeView, LoginCustomView

urlpatterns = [
    path('login/', LoginCustomView.as_view(), name='login'),
]
