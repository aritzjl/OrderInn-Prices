from django.contrib import admin
from .models import ModeloPrediccion, Prediccion, ScriptPrediccion

class ModeloPrediccionAdmin(admin.ModelAdmin):
    list_display = ('fecha_creacion', 'usuario')
    list_filter = ('fecha_creacion', 'usuario')
    search_fields = ('usuario__username',)
    date_hierarchy = 'fecha_creacion'

admin.site.register(ModeloPrediccion, ModeloPrediccionAdmin)

class PrediccionAdmin(admin.ModelAdmin):
    list_display = ('fecha_creacion', 'usuario', 'modelo_prediccion')
    list_filter = ('fecha_creacion', 'usuario', 'modelo_prediccion')
    search_fields = ('usuario__username', 'modelo_prediccion__id')
    date_hierarchy = 'fecha_creacion'

admin.site.register(Prediccion, PrediccionAdmin)

class ScriptPrediccionAdmin(admin.ModelAdmin):
    list_display = ('fecha_creacion', 'usuario', 'deleted')
    list_filter = ('fecha_creacion', 'usuario', 'deleted')
    search_fields = ('usuario__username',)
    date_hierarchy = 'fecha_creacion'
    
admin.site.register(ScriptPrediccion, ScriptPrediccionAdmin)