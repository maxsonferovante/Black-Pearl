# Generated by Django 4.2 on 2023-05-16 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convenios', '0006_contratacaoplanoodontologico_valor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contratacaoplanoodontologico',
            name='valor',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Valor'),
        ),
    ]
