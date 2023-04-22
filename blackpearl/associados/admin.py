from django.contrib import admin
from .models import Associado


@admin.register(Associado)
class AssociadoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sobrenome', 'slug', 'cpf', 'criado', 'ativo')
# Register your models here.

