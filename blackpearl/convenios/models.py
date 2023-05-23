from _decimal import Decimal
from django.db import models
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from django.urls import reverse

from blackpearl.associados.models import Associado, Dependente


# Create your models here.
class Base(models.Model):
    criado = models.DateField('Data de Criação', auto_now_add=True)
    modificado = models.DateField('Data de Atualização', auto_now_add=True)
    ativo = models.BooleanField('Ativo?', default=True)

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
    cartao = models.ForeignKey(CartaoConvenioVolus, on_delete=models.CASCADE, related_name='cartao')
    valor = models.DecimalField('Valor da Fatura', max_digits=8, decimal_places=2)
    valorComTaxa = models.DecimalField('Valor da Fatura com a Taxa Adm', max_digits=8, decimal_places=2, null=True,
                                       blank=True)
    competencia = models.DateField('Competência')

    def save(self, *args, **kwargs):
        taxa_administrativa = TaxasAdministrativa.objects.get(grupos='outros')

        percentual_taxa = taxa_administrativa.percentual
        taxa = 1 + (percentual_taxa / Decimal(100.0))
        self.valorComTaxa = self.valor * taxa
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Valor da fatura e competência: {}  / {}'.format(self.valor, self.competencia)


class PlanoOdontologico(Base):
    nome = models.CharField('Nome', default='Uniodonto Belém', max_length=20)
    numContrato = models.CharField('Número do contrato', max_length=20, default='00319')
    cnpj = models.CharField('CNPJ', max_length=40, default='15.308.521/0001-88')
    valorUnitario = models.DecimalField('Valor Unitário', max_digits=8, decimal_places=2)

    def __str__(self):
        return '{} - {}'.format(self.nome, self.numContrato)


class ContratacaoPlanoOdontologico(Base):
    contratante = models.OneToOneField(Associado, on_delete=models.CASCADE, related_name='plano_odontologico')
    plano_odontologico = models.ForeignKey(PlanoOdontologico, on_delete=models.CASCADE)
    dependentes = models.ManyToManyField(Dependente)
    valor = models.DecimalField('Valor', max_digits=8, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return '{} - {} - Plano: {}'.format(self.id, self.contratante, self.plano_odontologico)

@receiver(pre_save, sender=ContratacaoPlanoOdontologico)

def atualizar_valor_planoOdontologico(sender, instance, *args, **kwargs):
    valorPlano = PlanoOdontologico.objects.get(numContrato='00319').valorUnitario
    taxa = TaxasAdministrativa.objects.get(grupos=instance.contratante.associacao)
    try:
        instance.valor = ((valorPlano * (1 + instance.dependentes.count())) / (
                Decimal(100.0) - taxa.percentual)) * Decimal(100.0)
    except ValueError:
        instance.valor = (valorPlano / (Decimal(100.0) - taxa.percentual)) * Decimal(100.0)

@receiver(m2m_changed, sender=ContratacaoPlanoOdontologico.dependentes.through)
def atualizar_valor_planoOdontologico_dependentes(sender, instance, action, **kwargs):
    instance.save()


class Otica(Base):
    oticas_choices = [
        ('Ótica Telegrafo', 'Ótica Telegrafo'),
        ('Ótica Progressiva', 'Ótica Progressiva')
    ]
    nome = models.CharField('Nome da Ótica', max_length=40, choices=oticas_choices)
    cnpj = models.CharField('CNPJ', max_length=40)
    valorCompra = models.DecimalField('Valor da Compra', max_digits=8, decimal_places=2)


class TaxasAdministrativa(Base):
    ASSOCIACAO_CHOICES = [
        ('ag', 'Agredado(a)'),
        ('fiativo', 'Filiado(a) da Ativa'),
        ('fiaposent', 'Filiado(a) Aposentado(a)'),
        ('desfi', 'Desfiliado(a)'),
        ('outros', 'Cartão')
    ]

    grupos = models.CharField('Grupo', max_length=20, choices=ASSOCIACAO_CHOICES)
    percentual = models.DecimalField('Percetual da Taxa Administrativa (%)', max_digits=8, decimal_places=2)

    def __str__(self):
        return 'Taxa Administrativa: {}'.format(self.percentual)
