from datetime import timedelta

from django.utils import timezone
from blackpearl.convenios.models.planoSaudeModels import ContratoPlanoSaude
from blackpearl.convenios.models.planoOdontologicoModels import ContratoPlanoOdontologico
from blackpearl.cobrancas.models.faturaCobrancaModels import CobrancaPlanoSaude, CobrancaPlanoOdontologico, FaturaCobranca, PERCENTUAL_JUROS, PERCENTUAL_MULTA


class ProcessoFaturamentoService:
    @staticmethod
    def processar_faturamento_plano_saude():
        contratos_plano_saude = ContratoPlanoSaude.objects.filter(ativo=True)

        if contratos_plano_saude.exists() and  timezone.now().day == 29 and timezone.now().hour == 10 and timezone.now().minute == 20:
            for contrato in contratos_plano_saude:
                if not CobrancaPlanoSaude.objects.filter(contratoPlanoSaude=contrato).exists():

                    # Cálculo da data de vencimento para o próximo mês de maneira mais precisa
                    data_atual = timezone.now().date()
                    proximo_mes = data_atual.replace(day=29) + timedelta(days=35)  # Aproximadamente 35 dias para o próximo mês
                    data_vencimento = proximo_mes.replace(day=29)

                    CobrancaPlanoSaude.objects.create(
                        contratoPlanoSaude=contrato,
                        valorContratado=contrato.valorTotal,
                        dataDoVencimento= data_vencimento,
                        situacao='A',
                        juros= 0,
                        multa= 0
                    )
    @staticmethod
    def processar_faturamento_plano_odontologico():
        pass

