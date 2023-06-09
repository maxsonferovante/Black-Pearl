from django.contrib import admin
from .models import Associado, Empresa, Dependente

@admin.register(Associado)
class AssociadoAdmin(admin.ModelAdmin):
    list_display = ('nomecompleto', 'id','dataNascimento','cpf', 'empresa', 'matricula','criado', 'ativo')

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('id','nome', 'estado', 'criado', 'ativo')
@admin.register(Dependente)
class DependenteAdmin(admin.ModelAdmin):
    list_display = ('nomecompleto','id', 'dataNascimento', 'titular','criado', 'ativo')
