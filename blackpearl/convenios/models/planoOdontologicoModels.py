from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from blackpearl.associados.models import Associado
from blackpearl.convenios.models.models import Base, TaxasAdministrativa
from _decimal import Decimal

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
