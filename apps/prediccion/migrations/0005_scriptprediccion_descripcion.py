# Generated by Django 4.2.1 on 2023-12-21 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediccion', '0004_scriptprediccion_motivo_descarte'),
    ]

    operations = [
        migrations.AddField(
            model_name='scriptprediccion',
            name='descripcion',
            field=models.TextField(blank=True, null=True),
        ),
    ]
