from django.shortcuts import render, redirect
from crono.models import Piloto, Volta
from django.contrib import messages
from django.db.models import Q
from datetime import datetime

def cadastrar_piloto(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        numero_piloto = request.POST.get('numero_piloto')
        moto = request.POST.get('moto')
        categoria = request.POST.get('categoria')

        # Verifica se já existe um piloto com o mesmo nome ou número
        if Piloto.objects.filter(Q(nome=nome) | Q(numero_piloto=numero_piloto)).exists():
            messages.error(request, 'Já existe um piloto com esse nome ou número.')
        else:
            piloto = Piloto(nome=nome, numero_piloto=numero_piloto, moto=moto, categoria=categoria)
            piloto.save()
            messages.success(request, 'Piloto cadastrado com sucesso.')
            return redirect('cadastrar_piloto')

    return render(request, 'cadastrar_piloto.html')

def registrar_largada(request):
    if request.method == 'POST':
        numero_piloto = request.POST.get('numero_piloto')
        horario_largada= datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        numero_piloto= Piloto.objects.get(numero_piloto=numero_piloto)
        volta= Volta(horario_largada=horario_largada, numero_piloto=numero_piloto)
        volta.save()
        messages.success(request, 'Horario de largada cadastrado com sucesso')
        return redirect('registrar_largada')
    
    return render(request, 'registrar_largada.html')

def registrar_chegada(request):
    if request.method == 'POST':
        numero_piloto = request.POST.get('numero_piloto')
        horario_chegada= datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        numero_piloto= Piloto.objects.get(numero_piloto=numero_piloto)
        volta= Volta(horario_chegada=horario_chegada, numero_piloto=numero_piloto)
        volta.save()
        messages.success(request, 'Horario de chegada cadastrado com sucesso')
        return redirect('registrar_chegada')
    
    return render(request, 'registrar_chegada.html')



def exibir_pilotos(request):
    nome = request.GET.get('nome')
    numero_piloto = request.GET.get('numero_piloto')
    categoria = request.GET.get('categoria')
    if nome and numero_piloto and categoria:
        pilotos = Piloto.objects.filter(nome=nome, numero_piloto=numero_piloto, categoria=categoria)
    else:
        pilotos = Piloto.objects.all()
    return render(request, 'exibir_pilotos.html', {'pilotos': pilotos})

