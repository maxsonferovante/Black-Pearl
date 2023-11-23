from django.db import models
from django.urls import reverse
from blackpearl.associados.models import Associado, Dependente
from blackpearl.convenios.models.models import Base

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

