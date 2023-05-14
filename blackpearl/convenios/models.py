from _decimal import Decimal
from django.db import models

from blackpearl.associados.models import Associado

from datetime import datetime

# Create your models here.
class Base(models.Model):
    criado = models.DateField('Data de Criação', auto_now_add=True)
    modificado = models.DateField('Data de Atualização', auto_now_add=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True


planos_choices = [
    ('Unimed - Max Nacional', 'Unimed - Max Nacional'),
    ('Unimed - Grupo de Municipios', 'Unimed - Grupo de Municipios'),

]
segmentacao_choices = [
    ('Apartamento', 'Apartamento'),
    ('Enfermaria', 'Enfermaria')
]


class PlanoSaude(Base):
    nome = models.CharField("Nome do Plano", max_length=100, choices=planos_choices)
    cnpj = models.CharField('CNPJ', max_length=40, default="04.201.372/0001-37")
    contrato = models.CharField('Número do Contrato', max_length=10)
    segmentacao = models.CharField('Segmentação', max_length=20, choices=segmentacao_choices)
    atendimentoDomiciliar = models.BooleanField('Contratado?', default=False)
    valorAtendimentoDomiciliar = models.DecimalField("Valor do Atendimento Domiciliar", max_digits=5, decimal_places=2)

    def __str__(self):
        return '{} - {} - {}'.format(self.nome, self.contrato, self.segmentacao)


class ValoresPorFaixa(Base):
    planoSaude = models.ForeignKey(PlanoSaude, on_delete=models.CASCADE, related_name='faixas')
    idadeMin = models.IntegerField('Idade Minima')
    idadeMax = models.IntegerField('Idade Max')
    valor = models.DecimalField('Valor da Faixa', max_digits=6, decimal_places=2)

    def __str__(self):
        return '{} - {}:{}'.format(self.idadeMin, self.idadeMax, self.valor)


status_choices = [
    ('ATIVO', 'ATIVO'),
    ('SUSPENSO', 'SUSPENSO'),
    ('CANCELADO', 'CANCELADO')
]


class CartaoConvenioVolus(Base):
    nome = models.CharField('Nome do Cartão', max_length=20, default='Convênio Volus')
    titular = models.ForeignKey(Associado, on_delete=models.CASCADE, related_name='cartaovolus')
    valorLimite = models.DecimalField('Valor do Limite', max_digits=8, decimal_places=2)
    status = models.CharField('Status', max_length=20, choices=status_choices)
    def __str__(self):
        return '{}'.format(self.titular)

class FaturaCartao(Base):
    cartao = models.ForeignKey(CartaoConvenioVolus, on_delete=models.CASCADE, related_name='cartao')
    valor = models.DecimalField('Valor da Fatura', max_digits=8, decimal_places=2)
    valorComTaxa = models.DecimalField('Valor da Fatura com a Taxa Adm', max_digits=8, decimal_places=2,  null=True, blank=True)
    competencia = models.DateField('Competência')

    def save(self, *args, **kwargs):
        taxa_administrativa = TaxaAdministrativa.objects.get(categoria='Cartão')
        percentual_taxa = taxa_administrativa.percentual
        self.valorComTaxa = Decimal(self.valor * (1.0 + percentual_taxa / 100.0))
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Valor da fatura e competência: {}  / {}'.format(self.valor,self.competencia)

class PlanoOdontologico(Base):
    nome = models.CharField('Nome', default='Uniodonto Belém', max_length=20)
    numContrato = models.CharField('Número do contrato', max_length=20)
    cnpj = models.CharField('CNPJ', max_length=40, default='15.308.521/0001-88')
    valorUnitario = models.DecimalField('Valor Unitário', max_digits=8, decimal_places=2)

    def __str__(self):
        return 'Uniodonto Belém ({})'.format(self.numContrato)

oticas_choices = [
    ('Ótica Telegrafo', 'Ótica Telegrafo'),
    ('Ótica Progressiva', 'Ótica Progressiva')
]

class Otica(Base):
    nome = models.CharField('Nome da Ótica', max_length=40, choices=oticas_choices)
    cnpj = models.CharField('CNPJ', max_length=40)
    valorCompra = models.DecimalField('Valor da Compra', max_digits=8, decimal_places=2)
taxa_choices = [
    (15.0, '15%'),
    (8.0, '8%'),
    (5.0, '5%')
]
categoria_choices = [
    ('Cartão', 'Cartão'),
    ('Saúde', 'Saúde'),
    ('Odontológico','Odontológico')
]
class TaxaAdministrativa(Base):
    categoria = models.CharField('Categoria', max_length=20, choices=categoria_choices)
    percentual = models.DecimalField('Percetual da Taxa Administrativa', max_digits=8, decimal_places=2,
                                     choices=taxa_choices)

    def __str__(self):
        return 'Taxa Administrativa: {}'.format(self.percentual)
