from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from _decimal import Decimal
from blackpearl.associados.models import Associado
from blackpearl.convenios.models.models import TaxasAdministrativa, Base

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
    SITUACAOFATURA_CHOICES = [
        ('ABERTA', 'ABERTA'),
        ('PAGA', 'PAGA'),
        ('CANCELADA', 'CANCELADA')
    ]
    cartao = models.ForeignKey(CartaoConvenioVolus, on_delete=models.CASCADE, related_name='faturas')
    valor = models.DecimalField('Valor da Fatura', max_digits=8, decimal_places=2)
    valorComTaxa = models.DecimalField('Valor da Fatura com a Taxa Adm', max_digits=8, decimal_places=2, null=True,
                                       blank=True)
    competencia = models.DateField('Competência')

    situacaoFatura = models.CharField('Situação da Fatura', max_length=20, choices=SITUACAOFATURA_CHOICES,
                                      default=SITUACAOFATURA_CHOICES[0][0])
    def __str__(self):
        return 'Valor da fatura e competência: {}  / {}'.format(self.valor, self.competencia)


@receiver(pre_save, sender=FaturaCartao)
def aplicar_taxa_adm_cartao(sender, instance, *args, **kwargs):
    taxa_administrativa = TaxasAdministrativa.objects.get(grupos='outros')
    percentual_taxa = taxa_administrativa.percentual
    taxa = 1 + (percentual_taxa / Decimal(100.0))
    instance.valorComTaxa = instance.valor * taxa
