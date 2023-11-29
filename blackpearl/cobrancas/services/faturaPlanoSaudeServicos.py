from datetime import datetime

from blackpearl.cobrancas.models.faturasConvenios import FaturaPlanoSaude
from blackpearl.convenios.models.planoSaudeModels import ContratoPlanoSaude


class FaturaPlanoSaudeServicos:
    def __init__(self):
        self.fatura = FaturaPlanoSaude()
        self.contratos = ContratoPlanoSaude.objects.filter(ativo=True)

    def gerarFaturaPlanoSaude(self):
        # Salve a instância da fatura primeiro

        self.fatura.competencia = datetime.now()

        self.fatura.nome = "Fatura - Plano de Saúde " + self.fatura.competencia.strftime("%Y-%m-%d")

        self.fatura.valorTotalContratos = 0
        self.fatura.valorTotalAtendimentoDomiciliar = 0
        self.fatura.valorTotalAtendimentoTelefonico = 0
        self.fatura.valorTotalTaxaAdministrativa = 0
        self.fatura.valorTotal = 0

        for contrato in self.contratos:
            self.fatura.valorTotalContratos += contrato.valor

            if contrato.atendimentoDomiciliar:
                self.fatura.valorTotalAtendimentoDomiciliar += contrato.planoSaude.valorAtendimentoDomiciliar

            self.fatura.valorTotalAtendimentoTelefonico += contrato.planoSaude.valorAtendimentoTelefonico
            self.fatura.valorTotalTaxaAdministrativa += (contrato.valorTotal - contrato.valor)
            self.fatura.valorTotal += contrato.valorTotal

            self.fatura.save()

        for contrato in self.contratos:
            self.fatura.contratos.add(contrato)

        self.fatura.save()

    def converterFaturaParaJson(self):
        return {
            'id': self.fatura.id,
            'nome': self.fatura.nome,
            'competencia': self.fatura.competencia.strftime("%m/%Y"),
            'valorTotalContratos': self.fatura.valorTotalContratos,
            'valorTotalAtendimentoDomiciliar': self.fatura.valorTotalAtendimentoDomiciliar,
            'valorTotalAtendimentoTelefonico': self.fatura.valorTotalAtendimentoTelefonico,
            'valorTotalTaxaAdministrativa': self.fatura.valorTotalTaxaAdministrativa,
            'valorTotal': self.fatura.valorTotal
        }
