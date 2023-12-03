from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone

from blackpearl.convenios.models.planoSaudeModels import ContratoPlanoSaude
from blackpearl.convenios.models.planoOdontologicoModels import ContratoPlanoOdontologico
from blackpearl.cobrancas.models.faturaCobrancaModels import CobrancaPlanoSaude, CobrancaPlanoOdontologico, \
    PERCENTUAL_JUROS, PERCENTUAL_MULTA

TIME_MINUTES = 10


class ProcessoFaturamentoService(BackgroundScheduler):
    def __init__(self):
        super().__init__()

        self.add_job(self.processar_faturamento_plano_saude,
                     'interval', minutes=TIME_MINUTES, replace_existing=True,
                     max_instances=1)

        self.add_job(self.processar_faturamento_plano_odontologico,
                     'interval', minutes=TIME_MINUTES, replace_existing=True, max_instances=1)

        self.add_job(self.processar_faturas_vencidas,
                     'interval', minutes=TIME_MINUTES, replace_existing=True, max_instances=1)

        self.add_job(self.atualizar_juros_multas_faturas_vencidas,
                     'interval', minutes=TIME_MINUTES, replace_existing=True, max_instances=1)

    def __destroy__(self):
        self.shutdown()


    def gerar_data_vencimento(self):
        data_atual = timezone.now().date()

        # Obtendo o próximo mês
        proximo_mes = data_atual.replace(day=1)  # Indo para o primeiro dia do mês atual do datetime
        proximo_mes = proximo_mes + timezone.timedelta(days=32)  # Adicionando 32 dias (aproximadamente um mês)

        # Garantindo que a data seja o dia 10 do próximo mês
        data_vencimento = proximo_mes.replace(day=10)

        return data_vencimento


    def processar_faturamento_plano_saude(self):
        contratos_plano_saude = ContratoPlanoSaude.objects.filter(ativo=True)
        if contratos_plano_saude.exists():
            for contrato in contratos_plano_saude:
                # a data de vencimento é o dia 10 do mês seguinte
                data_vencimento = self.gerar_data_vencimento()
                if not CobrancaPlanoSaude.objects.filter(contratoPlanoSaude=contrato, dataDoVencimento = data_vencimento).exists():
                    CobrancaPlanoSaude.objects.create(
                        contratoPlanoSaude=contrato,
                        valorContratado=contrato.valorTotal,
                        valorPago=0,
                        dataDoVencimento=data_vencimento,
                        situacao='A',
                        juros=0,
                        multa=0
                    )


    def processar_faturamento_plano_odontologico(self):
        contratos_plano_odontologico = ContratoPlanoOdontologico.objects.filter(ativo=True)

        if contratos_plano_odontologico.exists():
            for contrato in contratos_plano_odontologico:
                # a data de vencimento é o dia 10 do mês seguinte
                data_vencimento = self.gerar_data_vencimento()
                if not CobrancaPlanoOdontologico.objects.filter(contratoPlanoOdontologico=contrato, dataDoVencimento = data_vencimento).exists():
                    CobrancaPlanoOdontologico.objects.create(
                        contratoPlanoOdontologico=contrato,
                        valorContratado=contrato.valor,
                        valorPago=0,
                        dataDoVencimento=data_vencimento,
                        situacao='A',
                        juros=0,
                        multa=0
                    )

    def processar_faturas_vencidas(self):
        cobrancas_plano_saude = CobrancaPlanoSaude.objects.filter(situacao='A',
                                                                  dataDoPagamento=None,
                                                                  contratoPlanoSaude__formaPagamento='Boleto Bancário')

        cobrancas_plano_odontologico = CobrancaPlanoOdontologico.objects.filter(situacao='A',
                                                                                dataDoPagamento=None,
                                                                                contratoPlanoOdontologico__formaPagamento='Boleto Bancário')

        todas_cobrancas = list(cobrancas_plano_saude) + list(cobrancas_plano_odontologico)

        for cobranca in todas_cobrancas:
            if cobranca.dataDoVencimento < timezone.now().date():
                print(cobranca)
                cobranca.situacao = 'V'
                cobranca.save()

    def atualizar_juros_multas_faturas_vencidas(self):

        cobrancas_plano_saude = CobrancaPlanoSaude.objects.filter(situacao='V',
                                                                  dataDoPagamento=None,
                                                                  contratoPlanoSaude__formaPagamento='Boleto Bancário')

        cobrancas_plano_odontologico = CobrancaPlanoOdontologico.objects.filter(situacao='V',
                                                                                dataDoPagamento=None,
                                                                                contratoPlanoOdontologico__formaPagamento='Boleto Bancário')

        todas_cobrancas = list(cobrancas_plano_saude) + list(cobrancas_plano_odontologico)

        for cobranca in todas_cobrancas:
            if cobranca.dataDoVencimento < timezone.now().date() and cobranca.situacao == 'V':
                print(cobranca)
                dias_atraso = timezone.now().date() - cobranca.dataDoVencimento

                cobranca.juros = cobranca.valorContratado * PERCENTUAL_JUROS * dias_atraso.days
                cobranca.multa = cobranca.valorContratado * PERCENTUAL_MULTA

                cobranca.valorPago = cobranca.valorContratado + cobranca.juros + cobranca.multa

                cobranca.save()

    @staticmethod
    def criar_fatura_plano_saude(contrato):
        data_atual = timezone.now().date()

        # Obtendo o próximo mês
        proximo_mes = data_atual.replace(day=1)  # Indo para o primeiro dia do mês atual do datetime
        proximo_mes = proximo_mes + timezone.timedelta(days=32)  # Adicionando 32 dias (aproximadamente um mês)

        # Garantindo que a data seja o dia 10 do próximo mês
        data_vencimento = proximo_mes.replace(day=10)

        CobrancaPlanoSaude.objects.create(
            contratoPlanoSaude=contrato,
            valorContratado=contrato.valorTotal,
            valorPago=0,
            dataDoVencimento=data_vencimento,
            situacao='A',
            juros=0,
            multa=0
        )

    @staticmethod
    def atualizar_valor_fatura_plano_saude(contrato):
        try:
            cobranca = CobrancaPlanoSaude.objects.get(contratoPlanoSaude=contrato, situacao='A')
            cobranca.valorContratado = contrato.valorTotal
            cobranca.save()
        except CobrancaPlanoSaude.DoesNotExist:
            ProcessoFaturamentoService.criar_fatura_plano_saude(contrato)


    @staticmethod
    def criar_fatura_plano_odontologico(contrato):
        data_atual = timezone.now().date()

        # Obtendo o próximo mês
        proximo_mes = data_atual.replace(day=1)  # Indo para o primeiro dia do mês atual do datetime
        proximo_mes = proximo_mes + timezone.timedelta(days=32)  # Adicionando 32 dias (aproximadamente um mês)

        # Garantindo que a data seja o dia 10 do próximo mês
        data_vencimento = proximo_mes.replace(day=10)
        CobrancaPlanoOdontologico.objects.create(
            contratoPlanoOdontologico=contrato,
            valorContratado=contrato.valor,
            valorPago=0,
            dataDoVencimento=data_vencimento,
            situacao='A',
            juros=0,
            multa=0
        )
        print("Criou fatura")

    @staticmethod
    def atualizar_valor_fatura_plano_odontologico(contrato):
        try:
            cobranca = CobrancaPlanoOdontologico.objects.get(contratoPlanoOdontologico=contrato, situacao='A')
            cobranca.valorContratado = contrato.valor
            cobranca.save()
        except CobrancaPlanoOdontologico.DoesNotExist:
            ProcessoFaturamentoService.criar_fatura_plano_odontologico(contrato)




