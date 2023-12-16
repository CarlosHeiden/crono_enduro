from django.urls import path
from . import views


urlpatterns = [
    path('cadastrar_piloto/', views.cadastrar_piloto, name='cadastrar_piloto'),
    path('exibir_pilotos/', views.exibir_pilotos, name='exibir_pilotos'),
    path(
        'registrar_largada/', views.registrar_largada, name='registrar_largada'
    ),
    path(
        'registrar_chegada/', views.registrar_chegada, name='registrar_chegada'
    ),
    path('resultados/', views.resultados, name='resultados'),
    path('resultados_por_categorias/',views.resultados_por_categorias, name='resultados_por_categorias'),
    path('resultado_piloto/',views.resultado_piloto, name='resultado_piloto'),
    path(
        'resultado_geral_tomada_tempo/',
        views.resultado_tomada_tempo,
        name='resultado_geral_tomada_tempo',
    ),
    path(
        'resultado_tomada_tempo_por_categorias/',
        views.resultado_tomada_tempo_por_categorias,
        name='resultado_tomada_tempo_por_categorias',
    ),
    path(
        'resultado_tomada_tempo_por_piloto/',
        views.resultado_tomada_tempo_por_piloto,
        name='resultado_tomada_tempo_por_piloto',
    ),
]
