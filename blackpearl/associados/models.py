from django.core.exceptions import ObjectDoesNotExist
from django.db import models
# Create your models here.

from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.urls import reverse

ESTADOS_CHOICES = [
    ("AC", "Acre"),
    ("AL", "Alagoas"),
    ("AP", "Amapá"),
    ("AM", "Amazonas"),
    ("BA", "Bahia"),
    ("CE", "Ceará"),
    ("DF", "Distrito Federal"),
    ("ES", "Espírito Santo"),
    ("GO", "Goiás"),
    ("MA", "Maranhão"),
    ("MT", "Mato Grosso"),
    ("MS", "Mato Grosso do Sul"),
    ("MG", "Minas Gerais"),
    ("PA", "Pará"),
    ("PB", "Paraíba"),
    ("PR", "Paraná"),
    ("PE", "Pernambuco"),
    ("PI", "Piauí"),
    ("RJ", "Rio de Janeiro"),
    ("RN", "Rio Grande do Norte"),
    ("RS", "Rio Grande do Sul"),
    ("RO", "Rondônia"),
    ("RR", "Roraima"),
    ("SC", "Santa Catarina"),
    ("SP", "São Paulo"),
    ("SE", "Sergipe"),
    ("TO", "Tocantins")
]

ORGEMISSOR_CHOICES = [
    ("SSP", "Secretaria de Segurança Pública"),
    ("SSPDS", "Secretaria de Segurança Pública e Defesa Social"),
    ("PF", "Polícia Federal"),
    ("PC", "Polícia Civil"),
    ("XXX", "Orgão Estrangeiro"),
    ("ZZZ", "Outro"),
]

ESTADOCIVIL_CHOICES = [
    ('S', 'Solteiro(a)'),
    ('C', 'Casado(a)'),
    ('D', 'Divorciado(a)'),
    ('V', 'Viúvo(a)'),
    ('U', 'União Estável'),
    ('O', 'Outro')
]

SEXO_CHOICES = [
('m', 'Masculino'),
('f', 'Feminino')

]

GRAUS_PARENTESCO_CHOICES = [
    ('P', 'Pai'),
    ('M', 'Mãe'),
    ('F', 'Filho(a)'),
    ('C', 'Cônjuge'),
    ('I', 'Irmão(ã)'),
    ('O', 'Outro'),
]

ASSOCIACAO_CHOICES = [
    ('ag', 'Agredado(a)'),
    ('fiativo', 'Filiado(a) da Ativa'),
    ('fiaposent', 'Filiado(a) Aposentado(a)'),
    ('func', 'Funcionário(a) da Associação'),
    ('desfi', 'Desfiliado(a)')
]

class Base(models.Model):
    criado = models.DateField('Data de Criação', auto_now_add=True)
    modificado = models.DateField('Data de Atualização', auto_now_add=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True

class Empresa(Base):
    nome = models.CharField('Nome da empresa', max_length= 100)
    estado = models.CharField('Estado de atuação', max_length=20, choices= ESTADOS_CHOICES)

    def __str__(self):
        return self.nome


class Associado(Base):
    DoesNotExist = None
    nomecompleto = models.CharField('Nome Completo', max_length=300)

    dataNascimento = models.DateField('Data de Nascimento')
    sexo = models.CharField('Sexo', max_length=1, choices=SEXO_CHOICES)

    cpf = models.CharField('CPF', max_length=11)
    identidade = models.CharField('Identidade', max_length=20, default='', blank=True)
    orgemissor = models.CharField('Órgão Emissor', max_length= 6, choices=ORGEMISSOR_CHOICES, default='',  blank=True)
    estadocivil = models.CharField('Estado Civil', max_length= 2, choices=ESTADOCIVIL_CHOICES, default='', blank=True)

    dataAssociacao = models.DateField('Data de Associação')
    associacao = models.CharField('Associação', max_length=50, choices=ASSOCIACAO_CHOICES, default= '')
    matricula = models.IntegerField('Matricula', blank=True, default=0)
    empresa  = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='empresa')

    email = models.EmailField('e-mail', )
    dddNumeroContato = models.CharField('DDD', max_length=2)
    numeroContato = models.CharField('Celular', max_length=9)

    slug = models.SlugField('Slug', max_length=100, blank=True, editable=False)

    # Endereço
    cep = models.CharField('CEP', max_length=9,  default='',  blank=True)
    logradouro = models.CharField('Logradouro', max_length=200, default='',  blank=True)
    num = models.IntegerField('Número', default='',  blank=True)
    bairro = models.CharField('Bairro', max_length=100, default='',  blank=True)
    cidade = models.CharField('Cidade', max_length=100, default='',  blank=True)
    estado = models.CharField('Estado (UF)', max_length=2, choices=ESTADOS_CHOICES, default='', blank=True)

    def save(self, *args, **kwargs):
        self.nomecompleto = self.nomecompleto.upper()
        self.logradouro = self.logradouro.upper()
        self.bairro = self.bairro.upper()
        self.cidade = self.cidade.upper()

        self.estado = self.estado.upper()

        super().save(*args, **kwargs)
    def __str__(self):
        return '{}'.format(self.nomecompleto.title())

    def get_nomecompleto_display(self):
        return self.nomecompleto.title()
    def get_sexo_display(self):
        return dict(SEXO_CHOICES)[self.sexo]
    def get_associacao_display(self):
        return dict(ASSOCIACAO_CHOICES)[self.associacao]
    def get_estadocivil_display(self):
        if self.estadocivil == '':
            return 'Não Informado'
        return dict(ESTADOCIVIL_CHOICES)[self.estadocivil]
    def get_absolute_url(self):
        return reverse("editar", kwargs={"pk": self.pk})

    def get_quantidade_dependentes(self):
        return self.dependentes.count()

class Dependente(Base):
    titular = models.ForeignKey(Associado, on_delete=models.CASCADE, related_name='dependentes')
    nomecompleto = models.CharField('Nome Completo', max_length=300)
    dataNascimento = models.DateField('Data de Nascimento')
    sexo = models.CharField('Sexo', max_length=1, choices=SEXO_CHOICES)

    cpf = models.CharField('CPF', max_length=11)
    identidade = models.CharField('Identidade', max_length=20, default='', blank=True)
    orgemissor = models.CharField('Órgão Emissor', max_length=6, choices=ORGEMISSOR_CHOICES, default='', blank=True)
    grauparentesco = models.CharField('Grau de Parentesco', max_length=6, choices=GRAUS_PARENTESCO_CHOICES, default='')


    def get_sexo_display(self):
        return dict(SEXO_CHOICES)[self.sexo]
    def get_grauparentesco_display(self):
        return dict(GRAUS_PARENTESCO_CHOICES)[self.grauparentesco]
    def get_nomecompleto_display(self):
        return self.nomecompleto.title()
    def get_absolute_url(self):
        return reverse("editar", kwargs={"pk": self.pk})
    def save(self, *args, **kwargs):
        self.nomecompleto = self.nomecompleto.upper()
        super().save(*args, **kwargs)
    def __str__(self):
        return '{} '.format(self.nomecompleto)
    ##dict(GRAUS_PARENTESCO_CHOICES)[self.grauparentesco].upper())
def associado_pre_save(instance, sender, **kwargs):
    instance.slug = slugify(instance.nomecompleto)
signals.pre_save.connect(associado_pre_save, sender=Associado)

def dependente_pre_save(instance, sender, **kwargs):
    instance.slug = slugify(instance.nomecompleto)
signals.pre_save.connect(dependente_pre_save, sender=Dependente)



class FileUploadExcelModel(Base):
    nome = models.CharField(max_length=100)
    arquivo = models.FileField()
