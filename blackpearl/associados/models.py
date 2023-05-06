from django.db import models
# Create your models here.

from django.db.models import signals
from django.template.defaultfilters import slugify

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

GRAUS_PARENTESCO_CHOICES = (
    ('P', 'Pai'),
    ('M', 'Mãe'),
    ('F', 'Filho(a)'),
    ('C', 'Cônjuge'),
    ('I', 'Irmão(ã)'),
    ('O', 'Outro'),
)

ASSOCIACAO_CHOICES = [
    ('ag', 'Agredado(a)'),
    ('fiativo', 'Filiado(a) da Ativa'),
    ('fiaposent', 'Filiado(a) Aposentado(a)'),
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
    estado = models.CharField('Estado de atuação', max_length=20)

    def __str__(self):
        return self.nome



class Associado(Base):
    nomecompleto = models.CharField('Nome Completo', max_length=300)

    dataNascimento = models.DateField('Data de Nascimento')
    sexo = models.CharField('Sexo', max_length=1, choices=SEXO_CHOICES)

    cpf = models.CharField('CPF', max_length=11)
    identidade = models.CharField('Identidade', max_length=20, default='')
    orgemissor = models.CharField('Órgão Emissor', max_length= 6, choices=ORGEMISSOR_CHOICES, default='')
    estadocivil = models.CharField('Estado Civil', max_length= 2, choices=ESTADOCIVIL_CHOICES, default='')

    dataAssociacao = models.DateField('Data de Associação')
    associacao = models.CharField('Associação', max_length=50, choices=ASSOCIACAO_CHOICES, default= '')
    matricula = models.IntegerField('Matricula', null=True)
    empresa  = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='empresa')

    email = models.EmailField('e-mail')
    dddNumeroContato = models.CharField('DDD', max_length=2)
    numeroContato = models.CharField('Celular', max_length=9)

    slug = models.SlugField('Slug', max_length=100, blank=True, editable=False)

    # Endereço
    cep = models.CharField('CEP', max_length=8)
    logradouro = models.CharField('Logradouro', max_length=200)
    num = models.IntegerField('Número')
    bairro = models.CharField('Bairro', max_length=100)
    cidade = models.CharField('Cidade', max_length=100)
    estado = models.CharField('Estado (UF)', max_length=2, choices=ESTADOS_CHOICES, default='')

    def __str__(self):
        return '{}'.format(self.nomecompleto)

class Dependente(Base):
    titular = models.ForeignKey(Associado, on_delete=models.CASCADE, related_name='dependentes')

    nomecompleto = models.CharField('Nome Completo', max_length=300)
    dataNascimento = models.DateField('Data de Nascimento', blank=True, null=True)
    sexo = models.CharField('Sexo', max_length=1, choices=SEXO_CHOICES)

    cpf = models.CharField('CPF', max_length=11)
    identidade = models.CharField('Identidade', max_length=20, default='')
    orgemissor = models.CharField('Órgão Emissor', max_length=6, choices=ORGEMISSOR_CHOICES, default='')
    grauparentesco = models.CharField('Grau de Parentesco', max_length=6, choices=GRAUS_PARENTESCO_CHOICES, default='')


def associado_pre_save(instance, sender, **kwargs):
    instance.slug = slugify(instance.nomecompleto)
signals.pre_save.connect(associado_pre_save, sender=Associado)

def dependente_pre_save(instance, sender, **kwargs):
    instance.slug = slugify(instance.nomecompleto)
signals.pre_save.connect(dependente_pre_save, sender=Dependente)



class FileUploadExcelModel(Base):
    nome = models.CharField(max_length=100)
    arquivo = models.FileField()
