from django import forms
from .models import Resultados, Piloto


class RegistrarLargadaForm(forms.Form):
    numero_piloto = forms.IntegerField(label='numero_piloto')


class RegistrarChegadaForm(forms.Form):
    numero_piloto = forms.IntegerField(label='numero_piloto')


class ResultadosForm(forms.ModelForm):
    class Meta:
        model = Resultados
        fields = '__all__'


class CadastrarPilotoForm(forms.Form):
    nome = forms.CharField(label='Nome')
    numero_piloto = forms.IntegerField(label='Número do piloto')
    moto = forms.CharField(label='Moto')
    categoria = forms.CharField(label='Categoria')
