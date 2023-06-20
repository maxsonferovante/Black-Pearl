from django.contrib import admin
from django import forms
from django.contrib import admin

from .models import ValoresPorFaixa, PlanoSaude, CartaoConvenioVolus, PlanoOdontologico, Otica, TaxasAdministrativa, \
    FaturaCartao, ContratoPlanoOdontologico, ContratoPlanoOdontologicoDependente, ContratoPlanoSaude


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
    list_display = ('contratante',
                    'id',
                    'planoOdontologico',
                    'valor',
                    'dataInicio',
                    'dataFim',
                    'ativo')


@admin.register(ContratoPlanoOdontologicoDependente)
class ContratoPlanoOdontologicoDependenteAdmin(admin.ModelAdmin):
    list_display = ('contrato',
                    'dependente',
                    'id',
                    'valor',
                    'dataInicio',
                    'dataFim',
                    'ativo')

@admin.register(ContratoPlanoSaude)
class ContratoPlanoSaudeAdmin(admin.ModelAdmin):
    list_display = ('contratante',
                    'id',
                    'planoSaude',
                    'faixa',
                    'valor',
                    'dataInicio',
                    'dataFim',
                    'ativo')