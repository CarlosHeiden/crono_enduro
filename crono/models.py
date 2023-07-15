from django.db import models
from django.utils import timezone

class Piloto(models.Model):
    nome = models.CharField(max_length=100)
    numero_piloto= models.IntegerField(default=None)
    moto =  models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome} ({self.numero_piloto})"


class RegistrarLargada(models.Model):
    id_volta = models.AutoField(primary_key=True)
    numero_piloto = models.ForeignKey(Piloto, on_delete=models.CASCADE, related_name='largadas')
    horario_largada = models.TimeField(null=True, blank=True)


class RegistrarChegada(models.Model):
    id_volta = models.AutoField(primary_key=True)
    numero_piloto = models.ForeignKey(Piloto, on_delete=models.CASCADE, related_name='chegadas')
    horario_chegada = models.TimeField(null=True, blank=True)


class Resultados(models.Model):

    nome = models.CharField(max_length=100)
    numero_piloto= models.IntegerField(default=None)
    moto =  models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    id_volta = models.IntegerField(default=0)
    horario_largada = models.TimeField(null=True, blank=True)
    horario_chegada = models.TimeField(null=True, blank=True)
    tempo_volta = models.DurationField(null=True, blank=True)
    tempo_total = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f"{self.nome} ({self.numero_piloto})"

   
class DadosCorrida(models.Model):
    nome = models.CharField(max_length=100)
    numero_piloto= models.IntegerField(default=None)
    moto =  models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    id_volta = models.AutoField(primary_key=True)
    horario_largada = models.TimeField(null=True, blank=True)
    horario_chegada = models.TimeField(null=True, blank=True)
    tempo_volta = models.DurationField(null=True, blank=True)
    tempo_total = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f"{self.nome} ({self.numero_piloto})"
    
    
  