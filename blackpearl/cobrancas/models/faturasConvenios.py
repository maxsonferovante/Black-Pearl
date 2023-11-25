from django.db import models
from .models import Base
from blackpearl.convenios.models.planoSaudeModels import ContratoPlanoSaude


class FaturaPlanoSaude(Base):
    nome = models.CharField('Nome', max_length=100, help_text='Nome da fatura. Ex: Fatura 01/2020')

    contratos = models.ManyToManyField(ContratoPlanoSaude, related_name='faturas')

    competencia = models.DateField('Competência',help_text='Data de competência da fatura. Ex: 01/2020')

    valorTotalContratos = models.DecimalField('Valor dos Contratos', max_digits=8, decimal_places=2)

    valorTotalAtendimentoDomiciliar = models.DecimalField('Valor do Atendimento Domiciliar', max_digits=8, decimal_places=2)

    valorTotalAtendimentoTelefonico = models.DecimalField('Valor do Atendimento Telefonico', max_digits=8, decimal_places=2)

    valorTotalTaxaAdministrativa = models.DecimalField('Valor da Taxa Administrativa', max_digits=8, decimal_places=2)

    valorTotal = models.DecimalField('Valor Total', max_digits=8, decimal_places=2)

    def __str__(self):
        return self.nome

