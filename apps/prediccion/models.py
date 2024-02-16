from django.db import models
from django.contrib.auth.models import User

class ModeloPrediccion(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    archivo_entrenamiento_excel = models.FileField(upload_to='archivos_entrenamiento/')
    archivo_modelo = models.FileField(upload_to='modelos_rf/')


class Prediccion(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    modelo_prediccion = models.ForeignKey(ModeloPrediccion, on_delete=models.CASCADE)
    archivo_output = models.FileField(upload_to='archivos_output/')


class ScriptPrediccion(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descripcion=models.TextField(blank=True,null=True)
    codigo=models.TextField(blank=True,null=True)
    deleted=models.BooleanField(default=False)
    motivo_descarte=models.TextField(blank=True,null=True)