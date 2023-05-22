from django.contrib.auth.decorators import login_required
from django.urls import path, include

from blackpearl.usuarios import views
from blackpearl.usuarios.views import HomeView, LoginCustomView

urlpatterns = [
    path('', LoginCustomView.as_view(), name='login'),
    path('home/', HomeView.as_view()),
]
