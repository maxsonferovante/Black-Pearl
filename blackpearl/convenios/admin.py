from django.contrib import admin
from django import forms
from django.contrib import admin

from .models import ValoresPorFaixa, PlanoSaude, CartaoConvenioVolus, PlanoOdontologico, Otica, TaxasAdministrativa, \
    FaturaCartao, ContratoPlanoOdontologico, ContratoPlanoOdontologicoDependete, ContratoPlanoSaude


# Register your models here.
@admin.register(ValoresPorFaixa)
class ValoresPorFaixaAdmin(admin.ModelAdmin):
    list_display = ('planoSaude', 'idadeMin', 'idadeMax', 'valor', 'ativo')


@admin.register(PlanoSaude)
class PlanoSaudeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'segmentacao', 'contrato', 'ativo')


@admin.register(CartaoConvenioVolus)
class CartaoConvenioAdmin(admin.ModelAdmin):
    list_display = ('titular', 'valorLimite', 'status', 'ativo')


@admin.register(FaturaCartao)
class FaturaCartaoAdmin(admin.ModelAdmin):
    list_display = ('cartao', 'valor', 'valorComTaxa', 'competencia')


@admin.register(PlanoOdontologico)
class PlanoOdontologicoUniodontoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'numContrato', 'valorUnitario', 'ativo')


@admin.register(Otica)
class oticaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'valorCompra', 'ativo')


@admin.register(TaxasAdministrativa)
class TaxasAdministrativaAdmin(admin.ModelAdmin):
    list_display = ('grupos', 'percentual', 'ativo', 'id')


@admin.register(ContratoPlanoOdontologico)
class ContratacaoPlanoOdontologicoAdmin(admin.ModelAdmin):
    list_display = ('contratante', 'plano_odontologico', 'valor','datacontrato',  'display_dependentes')

    def display_dependentes(self, obj):
        return ' / \n'.join([str(dependente) for dependente in obj.dependentes.all()])

    display_dependentes.short_description = 'Dependentes'

@admin.register(ContratoPlanoOdontologicoDependete)
class ContratoPlanoOdontologicoDependenteAdmin(admin.ModelAdmin):
    list_display = ['dependente', 'valor', 'datainclusao', 'titular_contratante']

@admin.register(ContratoPlanoSaude)
class ContratoPlanoSaudeAdmin(admin.ModelAdmin):
    list_display = ['contratante', 'plano', 'faixa', 'dataInclusao', 'valor','atendimentoDomiciliar', 'display_dependentes']
    def display_dependentes(self, obj):
        return ' / \n'.join([str(dependente) for dependente in obj.dependentes.all()])

    display_dependentes.short_description = 'Dependentes'

