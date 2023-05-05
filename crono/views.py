from django.shortcuts import render, redirect
from crono.models import Piloto, Volta
from django.contrib import messages

def cadastrar_piloto(request):
    if request.method == 'POST':
       nome= request.POST.get('nome')
       numero_piloto = request.POST.get('numero_piloto')
       moto= request.POST.get('moto')
       categoria= request.POST.get('categoria')
       piloto = Piloto(nome=nome, numero_piloto=numero_piloto, moto=moto, categoria=categoria)
       piloto.save()
       messages.success(request, 'Piloto cadastrado com sucesso')
       return redirect('cadastrar_piloto')
    return render(request,'cadastrar_piloto.html')

def exibir_pilotos(request):
    pilotos = Piloto.objects.all()
    return render(request, 'exibir_pilotos.html', {'pilotos': pilotos})


