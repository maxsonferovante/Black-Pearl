from decimal import Decimal

from django.db import models

from blackpearl.cobrancas.models.models import Base
from blackpearl.convenios.models.planoSaudeModels import ContratoPlanoSaude
from blackpearl.convenios.models.planoOdontologicoModels import ContratoPlanoOdontologico

PERCENTUAL_JUROS = Decimal(0.03)
PERCENTUAL_MULTA = Decimal(1.02)

CHOICES_SITUACAO = (
    ('A', 'Aberta'),
    ('P', 'Paga'),
    ('C', 'Cancelada'),
    ('V', 'Vencida'),
)

class FaturaCobranca(Base):
    valorContratado = models.DecimalField(verbose_name="Valor do contrato", max_digits=10, decimal_places=2)

    dataDoVencimento = models.DateField(verbose_name="Data do vencimento")

    dataDoPagamento = models.DateField(verbose_name="Data do pagamento", null=True, blank=True)
    situacao = models.CharField(verbose_name="Situação", max_length=1, choices=CHOICES_SITUACAO, default='A')

    juros = models.DecimalField(verbose_name="Juros", max_digits=10, decimal_places=2)
    multa = models.DecimalField(verbose_name="Multa", max_digits=10, decimal_places=2)

    def get_situacao(self):
        return CHOICES_SITUACAO[self.situacao][1]

    class Meta:
        verbose_name = "Cobrança"
        verbose_name_plural = "Cobranças"
        ordering = ['dataDoVencimento']

    def __str__(self):
        return self.valorContratado + " - " + self.dataDoVencimento


class CobrancaPlanoSaude(FaturaCobranca):
    contratoPlanoSaude = models.ForeignKey(ContratoPlanoSaude, verbose_name="Contrato do plano de saúde",
                                           on_delete=models.CASCADE)

    def __str__(self):
        return self.contratoPlanoSaude + " - " + self.valorContratado + " - " + self.dataDoVencimento


class CobrancaPlanoOdontologico(FaturaCobranca):
    contratoPlanoOdontologico = models.ForeignKey(ContratoPlanoOdontologico,
                                                  verbose_name="Contrato do plano odontológico",
                                                  on_delete=models.CASCADE)

    def __str__(self):
        return self.contratoPlanoOdontologico + " - " + self.valorContratado + " - " + self.dataDoVencimento
