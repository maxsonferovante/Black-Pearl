from django.db import models
from django.urls import reverse
from blackpearl.associados.models import Associado, Dependente
from blackpearl.convenios.models.models import Base


class PlanoOdontologico(Base):
    nome = models.CharField('Nome', default='Uniodonto Belém', max_length=20)
    numContrato = models.CharField('Número do contrato', max_length=20, default='00319')
    cnpj = models.CharField('CNPJ', max_length=40, default='15.308.521/0001-88')
    valorUnitario = models.DecimalField('Valor Unitário', max_digits=8, decimal_places=2)

    def __str__(self):
        return '{} - {}'.format(self.nome, self.numContrato)

class ContratoPlanoOdontologico(Base):

    contratante = models.OneToOneField(Associado, on_delete=models.CASCADE, related_name='contratos_odontologicos')
    planoOdontologico = models.ForeignKey(PlanoOdontologico, on_delete=models.CASCADE, related_name='contratos')
    valor = models.DecimalField('Valor', max_digits=8, decimal_places=2)
    formaPagamento = models.CharField('Forma de Pagamento', max_length=20, choices=[('Boleto Bancário', 'Boleto Bancário'),
                                                                                    ('Desconto em folha', 'Desconto em folha'),
                                                                                    ('Isento', 'Isento')])
    dataInicio = models.DateField('Data de Início')
    dataFim = models.DateField('Data de Fim', null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.contratante)

    def get_ativo_display(self):
        return 'Sim' if self.ativo else 'Não'

    def get_dataFim_display(self):
        if not self.dataFim:
            return "Vigente"
        else:
            return self.dataFim
    def get_absolute_url(self):
        return reverse("contrato_cadastrar", kwargs={"pk": self.pk})


class DependentePlanoOdontologico(Base):
    contratoTitular = models.ForeignKey(ContratoPlanoOdontologico, on_delete=models.CASCADE, related_name='dependentes')
    dependente = models.ForeignKey(Dependente, on_delete=models.CASCADE, related_name='contratos_odontologico_dependentes')
    valor = models.DecimalField('Valor', max_digits=8, decimal_places=2)
    valorComTaxa = models.DecimalField('Valor com Taxa', max_digits=8, decimal_places=2)
    dataInicio = models.DateField('Data de Início')
    dataFim = models.DateField('Data de Fim', null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.dependente)

    def get_dataFim_display(self):
        if not self.dataFim:
            return "Vigente"
        else:
            return self.dataFim

    def get_absolute_url(self):
        return reverse("dependente_cadastrar", kwargs={"pk": self.pk})

    def get_ativo_display(self):
        return 'Sim' if self.ativo else 'Não'

