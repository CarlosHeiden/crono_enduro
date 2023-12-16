from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from crono.models import Piloto, Categoria


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    list_filter = ('nome',)
    #search_fields = ('nome',)

class PilotoAdmin(ImportExportModelAdmin):
    # Define as colunas a serem exibidas na tabela de pilotos no painel de administração
    list_display = [
        'nome',
        'numero_piloto',
        'moto',
        'categoria',
    ]   
     # Define filtro por equipe na tabela de pilotos no painel de administração
    list_filter = [
        'nome',
        'numero_piloto',
        'moto',
        'categoria',
    ]  
     # Define busca por nome na tabela de pilotos no painel de administração
    search_fields = [
        'nome',
        'numero_piloto',
        'moto',
        'categoria',
    ]  


admin.site.register(Piloto, PilotoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
