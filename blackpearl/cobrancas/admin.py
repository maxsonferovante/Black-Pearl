from django.contrib import admin
from blackpearl.cobrancas.models.faturasConvenios import FaturaPlanoSaude
# Register your models here.


@admin.register(FaturaPlanoSaude)
class FaturaPlanoSaudeAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'nome',
                    'competencia',
                    'valorTotalContratos',
                    'valorTotalAtendimentoDomiciliar',
                    'valorTotalAtendimentoTelefonico',
                    'valorTotalTaxaAdministrativa',
                    'valorTotal',
                    'ativo')