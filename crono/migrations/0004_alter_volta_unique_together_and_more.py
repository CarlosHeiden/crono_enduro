# Generated by Django 4.2 on 2023-05-09 01:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crono', '0003_alter_piloto_nome_alter_piloto_numero_piloto'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='volta',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='volta',
            name='numero_volta',
        ),
    ]
