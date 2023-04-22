from django.db import models
# Create your models here.

from django.db.models import signals
from django.template.defaultfilters import slugify


class Base(models.Model):
    criado = models.DateField('Data de Criação', auto_now_add=True)
    modificado = models.DateField('Data de Atualização', auto_now_add=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True
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

class Associado(Base):

    nome = models.CharField('Nome', max_length=140)
    sobrenome = models.CharField('Sobrenome', max_length=260)
    dataNascimento = models.DateField('Data de Nascimento', blank=True, null=True)

    cpf = models.CharField('CPF', max_length=11)

    email = models.EmailField('e-mail')
    dddNumeroContato = models.CharField('DDD',max_length=2)
    numeroContato = models.CharField('Celular', max_length=9)
    slug = models.SlugField('Slug', max_length=100, blank=True, editable=False)

    # Endereço
    cep = models.CharField('CEP', max_length=8)
    logradouro = models.CharField('Logradouro', max_length=200)
    num = models.IntegerField('Número')
    bairro = models.CharField('Bairro', max_length=100)
    cidade = models.CharField('Cidade', max_length=100)
    estado = models.CharField('Estado (UF)',max_length=2, choices=ESTADOS_CHOICES, default='')

    def __str__(self):
        return self.nome

def associado_pre_save(instance, sender, **kwargs):
    instance.slug = slugify(instance.nome)

signals.pre_save.connect(associado_pre_save, sender=Associado)

class FileUploadExcelModel(Base):
    nome = models.CharField(max_length=100)
    arquivo = models.FileField()


