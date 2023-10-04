import datetime

from _decimal import Decimal
from django.db import models
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from django.urls import reverse


from blackpearl.associados.models import Associado, Dependente, ASSOCIACAO_CHOICES as ASSOCIACAO_CHOICES_ASSOCIADO


# Create your models here.
class Base(models.Model):
    criado = models.DateField('Data de Criação', auto_now_add=True)
    modificado = models.DateField('Data de Atualização', auto_now_add=True)
    ativo = models.BooleanField('Ativo?', default=True,  choices=[(True, 'Sim'), (False, 'Não')])

    class Meta:
        abstract = True


class PlanoSaude(Base):
    planos_choices = [
        ('Unimed - Max Nacional', 'Unimed - Max Nacional'),
        ('Unimed - Grupo de Municipios', 'Unimed - Grupo de Municipios'),

    ]
    segmentacao_choices = [
        ('Apartamento', 'Apartamento'),
        ('Enfermaria', 'Enfermaria')
    ]

    nome = models.CharField("Nome do Plano", max_length=100, choices=planos_choices)
    cnpj = models.CharField('CNPJ', max_length=40, default="04.201.372/0001-37")
    contrato = models.CharField('Número do Contrato', max_length=10)
    segmentacao = models.CharField('Segmentação', max_length=20, choices=segmentacao_choices)
    valorAtendimentoDomiciliar = models.DecimalField("Valor do Atendimento Domiciliar", max_digits=5, decimal_places=2)
    valorAtendimentoTelefonico = models.DecimalField("Valor do Atendimento Telefonico", max_digits=5, decimal_places=2, default=3.2)
    def __str__(self):
        return '{} - {}'.format(self.nome, self.segmentacao)


class ValoresPorFaixa(Base):
    planoSaude = models.ForeignKey(PlanoSaude, on_delete=models.CASCADE, related_name='faixas')
    idadeMin = models.IntegerField('Idade Minima')
    idadeMax = models.IntegerField('Idade Max')
    valor = models.DecimalField('Valor da Faixa', max_digits=6, decimal_places=2)

    def __str__(self):
        return '{} a {} (anos)'.format(self.idadeMin, self.idadeMax)

class ContratoPlanoSaude(Base):
    contratante = models.OneToOneField(Associado, on_delete=models.CASCADE, related_name='contratos_saude')
    planoSaude = models.ForeignKey(PlanoSaude, on_delete=models.CASCADE, related_name='contratos')

    faixa = models.ForeignKey(ValoresPorFaixa, on_delete=models.CASCADE, related_name='contratos_contratante')

    atendimentoDomiciliar = models.BooleanField('Atendimento Domiciliar', default=False, choices=[(True, 'Sim'), (False, 'Não')])

    dataInicio = models.DateField('Data da Contratação')
    dataFim = models.DateField('Data do Cancelamento', blank=True, null=True)

    formaPagamento = models.CharField('Forma de Pagamento', max_length=20,
                                      choices=[('Boleto Bancário', 'Boleto Bancário'),
                                               ('Desconto em folha', 'Desconto em folha'),
                                               ('Isento', 'Isento')])
    valor = models.DecimalField('Valor do Unitário', max_digits=8, decimal_places=2)
    valorTotal = models.DecimalField('Valor do Contrato', max_digits=8, decimal_places=2, null=True, blank=True)

    def get_atedimentoDomiciliar_display(self):
        if self.atendimentoDomiciliar:
            return 'Sim'
        else:
            return 'Não'
    def get_ativo_display(self):
        if self.ativo:
            return 'Sim'
        else:
            return 'Não'
    def dataFim_display(self):
        if self.dataFim:
            return self.dataFim
        else:
            return 'Vigente'
    def __str__(self):
        return '{} - {}'.format(self.contratante, self.planoSaude)

    def get_absolute_url(self):
        return reverse("contrato_cadastrar", kwargs={"pk": self.pk})
class ContratoPlanoSaudeDependente(Base):
    contrato = models.ForeignKey(ContratoPlanoSaude, on_delete=models.CASCADE, related_name='dependentes')
    dependente = models.OneToOneField(Dependente, on_delete=models.CASCADE, related_name='contrato_saude')
    valor = models.DecimalField('Valor Unitário', max_digits=8, decimal_places=2)
    dataInicio = models.DateField('Data de Início')
    dataFim = models.DateField('Data de Fim', null=True, blank=True)
    atendimentoDomiciliar = models.BooleanField('Atendimento Domiciliar', default=False,
                                                choices=[(True, 'Sim'), (False, 'Não')])

    faixa = models.ForeignKey(ValoresPorFaixa, on_delete=models.CASCADE, related_name='contratos_dependente')
    valorTotal = models.DecimalField('Valor do Contrato', max_digits=8, decimal_places=2, null=True, blank=True)
    def get__ativo_display(self):
        return 'Sim' if self.ativo else 'Não'

    def get__dataFim_display(self):
        if not self.dataFim:
            return "Vigente"
        else:
            return str(self.valor)


class CartaoConvenioVolus(Base):
    status_choices = [
        ('ATIVO', 'ATIVO'),
        ('SUSPENSO', 'SUSPENSO'),
        ('CANCELADO', 'CANCELADO')
    ]
    nome = models.CharField('Nome do Cartão', max_length=20, default='Convênio Volus')
    titular = models.ForeignKey(Associado, on_delete=models.CASCADE, related_name='cartaovolus')
    valorLimite = models.DecimalField('Valor do Limite', max_digits=8, decimal_places=2)
    status = models.CharField('Status', max_length=20, choices=status_choices)

    def __str__(self):
        return '{}'.format(self.titular)

    def get_absolute_url(self):
        return reverse("cartao_cadastrar", kwargs={"pk": self.pk})


class FaturaCartao(Base):
    cartao = models.ForeignKey(CartaoConvenioVolus, on_delete=models.CASCADE, related_name='faturas')
    valor = models.DecimalField('Valor da Fatura', max_digits=8, decimal_places=2)
    valorComTaxa = models.DecimalField('Valor da Fatura com a Taxa Adm', max_digits=8, decimal_places=2, null=True,
                                       blank=True)
    competencia = models.DateField('Competência')

    def __str__(self):
        return 'Valor da fatura e competência: {}  / {}'.format(self.valor, self.competencia)


@receiver(pre_save, sender=FaturaCartao)
def aplicar_taxa_adm_cartao(sender, instance, *args, **kwargs):
    taxa_administrativa = TaxasAdministrativa.objects.get(grupos='outros')
    percentual_taxa = taxa_administrativa.percentual
    taxa = 1 + (percentual_taxa / Decimal(100.0))
    instance.valorComTaxa = instance.valor * taxa


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

    quantidadeDependententes = models.IntegerField('Quantidade de Dependentes', default=0)

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


@receiver(pre_save, sender=ContratoPlanoOdontologico)
def atualizar_valor_planoOdontologico(sender, instance, *args, **kwargs):
    valorPlano = PlanoOdontologico.objects.get(numContrato='00319').valorUnitario
    taxa = TaxasAdministrativa.objects.get(grupos=instance.contratante.associacao)
    instance.valor = (valorPlano / (Decimal(100.0) - taxa.percentual)) * Decimal(100.0)

class Otica(Base):
    oticas_choices = [
        ('Ótica Telegrafo', 'Ótica Telegrafo'),
        ('Ótica Progressiva', 'Ótica Progressiva')
    ]
    nome = models.CharField('Nome da Ótica', max_length=40, choices=oticas_choices)
    cnpj = models.CharField('CNPJ', max_length=40)
    valorCompra = models.DecimalField('Valor da Compra', max_digits=8, decimal_places=2)


class TaxasAdministrativa(Base):
    ASSOCIACAO_CHOICES = ASSOCIACAO_CHOICES_ASSOCIADO

    grupos = models.CharField('Grupo', max_length=20, choices=ASSOCIACAO_CHOICES)
    percentual = models.DecimalField('Percetual da Taxa Administrativa (%)', max_digits=8, decimal_places=2)

    def __str__(self):
        return 'Taxa Administrativa: {}'.format(self.percentual)
