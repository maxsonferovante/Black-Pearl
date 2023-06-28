from django.contrib import admin
from .models import Diretor, Destinatario, Oficio


# Register your models here.
@admin.register(Diretor)
class DiretorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sobrenome', 'cargo', 'ativo')
    search_fields = ('nome', 'sobrenome', 'cargo')
    list_filter = ('ativo', 'cargo')

@admin.register(Destinatario)
class DestinatarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sobrenome', 'pronomeTratamento', 'cargo', 'ativo')
    search_fields = ('nome', 'sobrenome', 'pronomeTratamento', 'cargo')
    list_filter = ('ativo', 'pronomeTratamento')

@admin.register(Oficio)
class OficioAdmin(admin.ModelAdmin):
    list_display = ('numeracao', 'dataOficio', 'assunto', 'texto', 'remetente', 'destinatario', 'ativo')
    search_fields = ('numeracao', 'dataOficio', 'assunto', 'texto', 'remetente', 'destinatario')
    list_filter = ('ativo', 'dataOficio', 'remetente', 'destinatario')


