from django.contrib import admin
from .models import Associado, Empresa, Dependente


@admin.register(Associado)
class AssociadoAdmin(admin.ModelAdmin):
    list_display = ('nomecompleto', 'dataNascimento','cpf', 'empresa', 'criado', 'slug', 'ativo')

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'estado', 'criado', 'ativo')
@admin.register(Dependente)
class DependenteAdmin(admin.ModelAdmin):
    list_display = ('nomecompleto', 'dataNascimento', 'titular','criado', 'ativo')
