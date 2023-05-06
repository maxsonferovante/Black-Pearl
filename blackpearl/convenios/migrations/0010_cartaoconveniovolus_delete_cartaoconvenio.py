# Generated by Django 4.2 on 2023-05-06 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('associados', '0008_associado_matricula'),
        ('convenios', '0009_taxaadministrativa'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartaoConvenioVolus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Data de Criação')),
                ('modificado', models.DateField(auto_now_add=True, verbose_name='Data de Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('nome', models.CharField(default='Convênio Volus', max_length=20, verbose_name='Nome do Cartão')),
                ('valorLimite', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Valor do Limite')),
                ('status', models.CharField(choices=[('ATIVO', 'ATIVO'), ('SUSPENSO', 'SUSPENSO'), ('CANCELADO', 'CANCELADO')], max_length=20, verbose_name='Status')),
                ('titular', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cartaovolus', to='associados.associado')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='CartaoConvenio',
        ),
    ]
