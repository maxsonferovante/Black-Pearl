# Generated by Django 4.2 on 2023-11-25 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convenios', '0006_remove_contratoplanoodontologico_quantidadedependententes_and_more'),
        ('cobrancas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faturaplanosaude',
            name='contratos',
            field=models.ManyToManyField(blank=True, related_name='faturas', to='convenios.contratoplanosaude'),
        ),
    ]