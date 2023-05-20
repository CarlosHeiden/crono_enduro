from django import forms
from .models import Resultados

class RegistrarLargadaForm(forms.Form):
    numero_piloto = forms.IntegerField(label='numero_piloto')


class RegistrarChegadaForm(forms.Form):
     numero_piloto = forms.IntegerField(label='numero_piloto')

class ResultadosForm(forms.ModelForm):
    class Meta:
        model = Resultados
        fields = '__all__'
