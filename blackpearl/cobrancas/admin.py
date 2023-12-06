from django.contrib import admin
from .models.faturaCobrancaModels import FaturaCobranca, CobrancaPlanoSaude, CobrancaPlanoOdontologico, \
    FaturaCobrancaDiasConfig


# Register your models here.


@admin.register(FaturaCobranca)
class FaturaCobrancaAdmin(admin.ModelAdmin):
    list_display = ('valorContratado', 'dataDoVencimento', 'dataDoPagamento', 'situacao', 'juros', 'multa')
    list_filter = ('dataDoVencimento', 'dataDoPagamento', 'situacao')
    search_fields = ('valorContratado', 'dataDoVencimento', 'dataDoPagamento', 'situacao', 'juros', 'multa')


@admin.register(CobrancaPlanoSaude)
class CobrancaPlanoSaudeAdmin(admin.ModelAdmin):
    list_display = (
    'contratoPlanoSaude', 'valorContratado', 'dataDoVencimento', 'dataDoPagamento', 'situacao', 'juros', 'multa')
    list_filter = ('dataDoVencimento', 'dataDoPagamento', 'situacao')
    search_fields = (
    'contratoPlanoSaude', 'valorContratado', 'dataDoVencimento', 'dataDoPagamento', 'situacao', 'juros', 'multa')


@admin.register(CobrancaPlanoOdontologico)
class CobrancaPlanoOdontologicoAdmin(admin.ModelAdmin):
    list_display = (
    'contratoPlanoOdontologico', 'valorContratado', 'dataDoVencimento', 'dataDoPagamento', 'situacao', 'juros', 'multa')
    list_filter = ('dataDoVencimento', 'dataDoPagamento', 'situacao')
    search_fields = (
    'contratoPlanoOdontologico', 'valorContratado', 'dataDoVencimento', 'dataDoPagamento', 'situacao', 'juros', 'multa')


@admin.register(FaturaCobrancaDiasConfig)
class FaturaCobrancaDiasConfigAdmin(admin.ModelAdmin):
    """
        class FaturaCobrancaDiasConfig(Base):
        diaParaGeracaoPlanosDeSaude = models.IntegerField(verbose_name="Dia para geração dos planos de saúde",
                                                          default=15)
        diaParaGeracaoPlanosOdontologicos = models.IntegerField(
            verbose_name="Dia para geração dos planos odontológicos",
            default=15)

        diaParaVencimentoPlanosDeSaude = models.IntegerField(verbose_name="Dia para vencimento dos planos de saúde",
                                                             default=10)
        diaParaVencimentoPlanosOdontologico = models.IntegerField(
            verbose_name="Dia para vencimento dos planos odontológicos", default=10)
    """
    list_display = (
    'diaParaGeracaoPlanosDeSaude',
    'diaParaGeracaoPlanosOdontologico',
    'diaParaVencimentoPlanosDeSaude',
    'diaParaVencimentoPlanosOdontologico'
    )
