from django.apps import AppConfig


class CobrancasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blackpearl.cobrancas'

    def ready(self):
        from blackpearl.cobrancas.services.processoFaturamentoService import ProcessoFaturamentoService
        processoFaturamentoService = ProcessoFaturamentoService()

        processoFaturamentoService.start()

