# Generated by Django 4.2 on 2023-05-18 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crono', '0002_rename_registrar_chegada_registrarchegada_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrarchegada',
            name='id',
        ),
        migrations.RemoveField(
            model_name='registrarlargada',
            name='id',
        ),
        migrations.AlterField(
            model_name='registrarchegada',
            name='id_volta',
            field=models.IntegerField(
                default=None, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name='registrarlargada',
            name='id_volta',
            field=models.IntegerField(
                default=None, primary_key=True, serialize=False
            ),
        ),
    ]
