from django.contrib import admin
from .models import ValoresPorFaixa, PlanoSaude, CartaoConvenioVolus, PlanoOdontologico, Otica, TaxaAdministrativa, \
    FaturaCartao,ContratacaoPlanoOdontologico, ContratacaoDependentePlanoOdontologico


# Register your models here.
@admin.register(ValoresPorFaixa)
class ValoresPorFaixaAdmin(admin.ModelAdmin):
    list_display = ('planoSaude','idadeMin', 'idadeMax', 'valor', 'ativo')

@admin.register(PlanoSaude)
class PlanoSaudeAdmin(admin.ModelAdmin):
    list_display = ('nome','cnpj', 'segmentacao', 'contrato', 'ativo')

@admin.register(CartaoConvenioVolus)
class CartaoConvenioAdmin(admin.ModelAdmin):
    list_display = ('titular', 'valorLimite','status', 'ativo')

@admin.register(FaturaCartao)
class FaturaCartaoAdmin(admin.ModelAdmin):
    list_display = ('cartao', 'valor','valorComTaxa', 'competencia')

@admin.register(PlanoOdontologico)
class PlanoOdontologicoUniodontoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj','numContrato', 'valorUnitario', 'ativo')


@admin.register(Otica)
class oticaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'valorCompra', 'ativo')

@admin.register(TaxaAdministrativa)
class TaxaAdministrativaAdmin(admin.ModelAdmin):
    list_display = ('categoria','percentual', 'ativo')


@admin.register(ContratacaoPlanoOdontologico)
class ContratacaoPlanoOdontologicoAdmin(admin.ModelAdmin):
    list_display = ('contratante', 'plano_odontologico', 'display_dependentes', 'valor')

    def display_dependentes(self, obj):
        return ', '.join([str(dependente) for dependente in obj.dependentes.all()])

    display_dependentes.short_description = 'Dependentes'
@admin.register(ContratacaoDependentePlanoOdontologico)
class ContratacaoDependentePlanoOdontologico(admin.ModelAdmin):
    list_display = ('dependente' , 'contratacao_plano_odontologico', 'valor')