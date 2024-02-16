from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name = "home"),
    path('crear-prediccion/',views.crear_prediccion,name = "crear_prediccion"),
    path('entrenar-modelo/',views.entrenar_modelo,name = "entrenar_modelo"),
    path('actualizar/',views.actualizar,name = "actualizar"),
    path('descartar/',views.descartar,name = "descartar"),
]
