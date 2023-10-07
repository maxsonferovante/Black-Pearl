from django.db import models
from blackpearl.associados.models import ASSOCIACAO_CHOICES as ASSOCIACAO_CHOICES_ASSOCIADO


# Create your models here.
class Base(models.Model):
    criado = models.DateField('Data de Criação', auto_now_add=True)
    modificado = models.DateField('Data de Atualização', auto_now_add=True)
    ativo = models.BooleanField('Ativo?', default=True,  choices=[(True, 'Sim'), (False, 'Não')])

    class Meta:
        abstract = True



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
