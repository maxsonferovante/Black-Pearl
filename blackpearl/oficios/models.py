from django.db import models
from django.db.models import signals
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.db.models import signals

# Create your models here.
class Base(models.Model):
    criado = models.DateField('Data de Criação', auto_now_add=True)
    modificado = models.DateField('Data de Atualização', auto_now_add=True)
    ativo = models.BooleanField('Ativo?', default=True,  choices=[(True, 'Sim'), (False, 'Não')])

    class Meta:
        abstract = True

class Diretor(Base):
    CARGO_CHOICES = [
        ('Presidente', 'Presidente'),
        ('Vice-Presidente', 'Vice-Presidente'),
        ('1º Tesoureiro', '1º Tesoureiro'),
        ('2º Tesoureiro', '2º Tesoureiro'),
        ('1º Secretário', '1º Secretário'),
        ('2º Secretário', '2º Secretário'),
    ]
    nome = models.CharField('Nome do Diretor', max_length=100)
    sobrenome = models.CharField('Sobrenome do Diretor', max_length=100)
    email = models.EmailField('E-mail', max_length=100)

    cargo = models.CharField('Cargo', max_length=100, choices=CARGO_CHOICES)
    photo = models.ImageField(upload_to='oficios/diretores', verbose_name='Foto', null=True, blank=True)
    assinatura = models.ImageField(upload_to='oficios/assinaturas', verbose_name='Assinatura', null=True, blank=True)

    slug = models.SlugField(max_length=100, blank=True, unique=True)
    
    def __str__(self):
        return '{} {}'.format(self.nome, self.sobrenome)

    def get_nome_sobrenome(self):
        return '{} {}'.format(self.nome, self.sobrenome)
    
    def get_absolute_url(self):
        return reverse('diretor', kwargs={'slug': self.slug})
    
    

def slug_pre_save(signal, instance, sender, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.nome + ' ' + instance.sobrenome)

signals.pre_save.connect(slug_pre_save, sender=Diretor)


class Destinatario(Base):
    PRONOME_TRATAMENTO_CHOICES = [
        ('Sr.', 'Sr.'),
        ('Sra.', 'Sra.'),
    ]
    nome = models.CharField('Nome do Destinatário', max_length=100)
    sobrenome = models.CharField('Sobrenome do Destinatário', max_length=100)
    email = models.EmailField('E-mail', max_length=100)

    pronomeTratamento = models.CharField('Pronome de Tratamento', max_length=100,
                                         choices=PRONOME_TRATAMENTO_CHOICES)

    cargo = models.CharField('Cargo', max_length=100)
    def __str__(self):
        return '{} {}'.format(self.nome, self.sobrenome)

    def get_nome_sobrenome(self):
        return '{} {}'.format(self.nome, self.sobrenome)

class Oficio(Base):
    numeracao = models.IntegerField('Numeração do Ofício')
    dataOficio = models.DateField('Data do Ofício')
    assunto = models.CharField('Assunto', max_length=200)
    texto = models.TextField('Texto')
    remetente = models.ForeignKey(Diretor, on_delete=models.CASCADE, verbose_name='remetente')
    destinatario = models.ForeignKey(Destinatario, on_delete=models.CASCADE, verbose_name='destinatario')

    def get_dataOficioYear(self):
        return self.dataOficio.strftime('%Y')