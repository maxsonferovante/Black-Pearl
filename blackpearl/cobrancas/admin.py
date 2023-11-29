from django.contrib import admin
from .models.faturaCobrancaModels import FaturaCobranca, CobrancaPlanoSaude, CobrancaPlanoOdontologico
# Register your models here.


@admin.register(FaturaCobranca)
class FaturaCobrancaAdmin(admin.ModelAdmin):
    list_display = ('valorContratado', 'dataDoVencimento', 'dataDoPagamento', 'situacao', 'juros', 'multa')
    list_filter = ('dataDoVencimento', 'dataDoPagamento', 'situacao')
    search_fields = ('valorContratado', 'dataDoVencimento', 'dataDoPagamento', 'situacao', 'juros', 'multa')

@admin.register(CobrancaPlanoSaude)
class CobrancaPlanoSaudeAdmin(admin.ModelAdmin):
    list_display = ('contratoPlanoSaude', 'valorContratado', 'dataDoVencimento', 'dataDoPagamento', 'situacao', 'juros', 'multa')
    list_filter = ('dataDoVencimento', 'dataDoPagamento', 'situacao')
    search_fields = ('contratoPlanoSaude', 'valorContratado', 'dataDoVencimento', 'dataDoPagamento', 'situacao', 'juros', 'multa')

@admin.register(CobrancaPlanoOdontologico)
class CobrancaPlanoOdontologicoAdmin(admin.ModelAdmin):
    list_display = ('contratoPlanoOdontologico', 'valorContratado', 'dataDoVencimento', 'dataDoPagamento', 'situacao', 'juros', 'multa')
    list_filter = ('dataDoVencimento', 'dataDoPagamento', 'situacao')
    search_fields = ('contratoPlanoOdontologico', 'valorContratado', 'dataDoVencimento', 'dataDoPagamento', 'situacao', 'juros', 'multa')



