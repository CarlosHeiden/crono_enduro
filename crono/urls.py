from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar_piloto/', views.cadastrar_piloto, name='cadastrar_piloto'),
    path('exibir_pilotos/', views.exibir_pilotos, name='exibir_pilotos'),
]