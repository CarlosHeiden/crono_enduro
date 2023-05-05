from django.db import models


class Piloto(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    numero_piloto= models.IntegerField(default=None, unique=True)
    moto =  models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome} ({self.numero})"

class Volta(models.Model):
    numero_piloto = models.ForeignKey(Piloto, on_delete=models.CASCADE, related_name='voltas')
    numero_volta = models.IntegerField()
    horario_largada = models.DateTimeField(null=True, blank=True)
    horario_chegada = models.DateTimeField(null=True, blank=True)
    tempo_volta = models.DateTimeField(null=True, blank=True)
    tempo_acumulado = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('numero_piloto', 'numero_volta')
