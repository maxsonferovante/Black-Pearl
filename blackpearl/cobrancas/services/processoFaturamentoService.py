from datetime import timedelta

from django.utils import timezone
from blackpearl.convenios.models.planoSaudeModels import ContratoPlanoSaude
from blackpearl.convenios.models.planoOdontologicoModels import ContratoPlanoOdontologico
from blackpearl.cobrancas.models.faturaCobrancaModels import CobrancaPlanoSaude, CobrancaPlanoOdontologico, FaturaCobranca, PERCENTUAL_JUROS, PERCENTUAL_MULTA

dia_geracao_fatura = 29
hora_geracao_fatura = 23
minuto_geracao_fatura = 00

class ProcessoFaturamentoService:
    @staticmethod
    def processar_faturamento_plano_saude():
        print ("processar_faturamento_plano_saude")
        contratos_plano_saude = ContratoPlanoSaude.objects.filter(ativo=True)

        if contratos_plano_saude.exists() and  timezone.now().day == dia_geracao_fatura and timezone.now().hour == hora_geracao_fatura and timezone.now().minute == minuto_geracao_fatura:
            for contrato in contratos_plano_saude:
                if not CobrancaPlanoSaude.objects.filter(contratoPlanoSaude=contrato).exists():

                    # Cálculo da data de vencimento para o próximo mês de maneira mais precisa
                    data_atual = timezone.now().date()
                    proximo_mes = data_atual.replace(day=29) + timedelta(days=35)  # Aproximadamente 35 dias para o próximo mês
                    data_vencimento = proximo_mes.replace(day=29)

                    CobrancaPlanoSaude.objects.create(
                        contratoPlanoSaude=contrato,
                        valorContratado=contrato.valorTotal,
                        valorPago = 0,
                        dataDoVencimento= data_vencimento,
                        situacao='A',
                        juros= 0,
                        multa= 0
                    )

    @staticmethod
    def processar_faturamento_plano_odontologico():
        print ("processar_faturamento_plano_odontologico")
        contratos_plano_odontologico = ContratoPlanoOdontologico.objects.filter(ativo=True)

        if contratos_plano_odontologico.exists()and  timezone.now().day == dia_geracao_fatura and timezone.now().hour == hora_geracao_fatura and timezone.now().minute == minuto_geracao_fatura:
            for contrato in contratos_plano_odontologico:
                if not CobrancaPlanoOdontologico.objects.filter(contratoPlanoOdontologico=contrato).exists():

                    # Cálculo da data de vencimento para o próximo mês de maneira mais precisa
                    data_atual = timezone.now().date()
                    proximo_mes = data_atual.replace(day=29) + timedelta(days=35)
                    data_vencimento = proximo_mes.replace(day=29)

                    CobrancaPlanoOdontologico.objects.create(
                        contratoPlanoOdontologico=contrato,
                        valorContratado=contrato.valorTotal,
                        valorPago = 0,
                        dataDoVencimento=data_vencimento,
                        situacao='A',
                        juros= 0,
                        multa= 0
                    )

    @staticmethod
    def processar_faturamento():
        print ("processar_faturamento")
        ProcessoFaturamentoService.processar_faturamento_plano_saude()
        ProcessoFaturamentoService.processar_faturamento_plano_odontologico()

    @staticmethod
    def processar_faturas_vencidas():
        print("processar_faturas_vencidas")
        cobrancas_plano_saude = CobrancaPlanoSaude.objects.filter(situacao='A')
        cobrancas_plano_odontologico = CobrancaPlanoOdontologico.objects.filter(situacao='A')

        todas_cobrancas = list(cobrancas_plano_saude) + list(cobrancas_plano_odontologico)

        for cobranca in todas_cobrancas:
            if cobranca.dataDoVencimento < timezone.now().date() and cobranca.situacao == 'A':
                cobranca.situacao = 'V'
                cobranca.valorPago = cobranca.valorContratado
                cobranca.save()

    @staticmethod
    def atualizar_juros_multas_faturas_vencidas():
        print("atualizar_juros_multas_faturas_vencidas")
        cobrancas_plano_saude = CobrancaPlanoSaude.objects.filter(situacao='V')
        cobrancas_plano_odontologico = CobrancaPlanoOdontologico.objects.filter(situacao='V')

        todas_cobrancas = list(cobrancas_plano_saude) + list(cobrancas_plano_odontologico)

        for cobranca in todas_cobrancas:
            if cobranca.dataDoVencimento < timezone.now().date() and cobranca.situacao == 'V':
                dias_atraso = timezone.now().date() - cobranca.dataDoVencimento
                cobranca.juros = cobranca.valorContratado * PERCENTUAL_JUROS * dias_atraso.days
                cobranca.multa = cobranca.valorContratado * PERCENTUAL_MULTA
                cobranca.valorPago = cobranca.valorContratado + cobranca.juros + cobranca.multa
                cobranca.save()

