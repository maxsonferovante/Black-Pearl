from django.apps import AppConfig

class CobrancasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blackpearl.cobrancas'

    def ready(self):
        from blackpearl.cobrancas.services.processoFaturamentoService import ProcessoFaturamentoService
        try:
            processoFaturamentoService = ProcessoFaturamentoService()
            processoFaturamentoService.start()
        except Exception as e:
            # Log the error and retry later
            print(f"Error starting ProcessoFaturamentoService: {e}")
            # scheduler.add_job(processoFaturamentoService.start, 'interval', seconds=30)
