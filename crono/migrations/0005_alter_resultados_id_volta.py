# Generated by Django 4.2 on 2023-05-18 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crono', '0004_alter_registrarchegada_id_volta_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultados',
            name='id_volta',
            field=models.IntegerField(default=0),
        ),
    ]
