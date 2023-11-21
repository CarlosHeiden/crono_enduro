from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from crono.models import Piloto


class PilotoAdmin(ImportExportModelAdmin):
    list_display = [
        'nome',
        'numero_piloto',
        'moto',
        'categoria',
    ]   # Define as colunas a serem exibidas na tabela de pilotos no painel de administração
    list_filter = [
        'nome',
        'numero_piloto',
        'moto',
        'categoria',
    ]   # Define filtro por equipe na tabela de pilotos no painel de administração
    search_fields = [
        'nome',
        'numero_piloto',
        'moto',
        'categoria',
    ]   # Define busca por nome na tabela de pilotos no painel de administração



admin.site.register(Piloto, PilotoAdmin)
