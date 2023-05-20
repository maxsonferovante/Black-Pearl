# Generated by Django 4.2 on 2023-05-20 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('associados', '0001_initial'),
        ('convenios', '0020_taxasadministrativa_delete_taxaadministrativa'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContratacaoDependentePlanoOdontologico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Data de Criação')),
                ('modificado', models.DateField(auto_now_add=True, verbose_name='Data de Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('valor', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Valor')),
                ('contratacao_plano_odontologico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='convenios.contratacaoplanoodontologico')),
                ('dependente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='associados.dependente')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
