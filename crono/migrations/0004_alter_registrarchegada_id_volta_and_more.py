# Generated by Django 4.2 on 2023-05-18 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crono', '0003_remove_registrarchegada_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrarchegada',
            name='id_volta',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='registrarlargada',
            name='id_volta',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
