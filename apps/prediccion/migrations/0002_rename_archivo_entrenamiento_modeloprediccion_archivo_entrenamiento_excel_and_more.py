# Generated by Django 5.0 on 2023-12-14 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prediccion', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='modeloprediccion',
            old_name='archivo_entrenamiento',
            new_name='archivo_entrenamiento_excel',
        ),
        migrations.RenameField(
            model_name='modeloprediccion',
            old_name='archivo_rf',
            new_name='archivo_modelo',
        ),
    ]
