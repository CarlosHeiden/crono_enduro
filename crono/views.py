from django.shortcuts import render, redirect
from models import Piloto, Volta


def cadastrar_piloto(request):
    if request == 'POST':
       nome= request.POST.get('nome')
       numero_piloto = request.POST.get('numero_piloto')
       moto= request.POST.get('moto')
       categoria= request.POST.get('categoria')
       piloto = Piloto(nome=nome, numero_piloto=numero_piloto, moto=moto, categoria=categoria)
       piloto.save
       return redirect('exibir_pilotos')
    return render(request='cadastrar_piloto.html')


