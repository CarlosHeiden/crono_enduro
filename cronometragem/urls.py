"""
URL configuration for cronometragem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from crono.urls import *

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('cadastrar_piloto/', views.cadastrar_piloto, name='cadastrar_piloto'),
    path('exibir_pilotos/', views.exibir_pilotos, name='exibir_pilotos'),
    path('registrar_largada/', views.registrar_largada, name='registrar_largada'),
    path('registrar_chegada/', views.registrar_chegada, name='registrar_chegada'),
    path('resultados/', views.resultados, name='resultados'),
    path('resultado_piloto/', views.resultado_piloto, name='resultado_piloto'),
]

