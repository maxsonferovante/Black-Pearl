# Generated by Django 4.2 on 2023-05-16 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convenios', '0003_alter_contratacaoplanoodontologico_contratacao_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contratacaoplanoodontologico',
            old_name='contratacao',
            new_name='contratante',
        ),
    ]