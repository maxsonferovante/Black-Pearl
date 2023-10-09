from django.contrib import admin
from django import forms
from django.contrib import admin

from blackpearl.convenios.models.planoSaudeModels import PlanoSaude, ContratoPlanoSaude, ContratoPlanoSaudeDependente, ValoresPorFaixa
from blackpearl.convenios.models.planoOdontologicoModels import ContratoPlanoOdontologico, PlanoOdontologico, \
    DependentePlanoOdontologico
from blackpearl.convenios.models.models import TaxasAdministrativa, Otica
from blackpearl.convenios.models.cartaoVolusModels import CartaoConvenioVolus, FaturaCartao

@admin.register(TaxasAdministrativa)
class TaxasAdministrativaAdmin(admin.ModelAdmin):
    list_display = ('grupos', 'percentual', 'ativo', 'id')


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



@admin.register(ContratoPlanoOdontologico)
class ContratacaoPlanoOdontologicoAdmin(admin.ModelAdmin):
    list_display = ('contratante',
                    'id',
                    'planoOdontologico',
                    'valor',
                    'dataInicio',
                    'dataFim',
                    'ativo')


@admin.register(DependentePlanoOdontologico)
class DependentePlanoOdontologicoAdmin(admin.ModelAdmin):
    list_display = ('contratoTitular',
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
                    'valorTotal',
                    'dataInicio',
                    'dataFim',
                    'ativo')

@admin.register(ContratoPlanoSaudeDependente)
class ContratoPlanoSaudeDependenteAdmin(admin.ModelAdmin):
    list_display = ('contrato',
                    'dependente',
                    'id',
                    'valor',
                    'valorTotal',
                    'dataInicio',
                    'dataFim',
                    'ativo')