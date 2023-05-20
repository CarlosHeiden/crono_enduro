from django.shortcuts import render, redirect
from crono.models import Piloto, RegistrarLargada, RegistrarChegada, Resultados
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta, timezone, date
from crono.forms import RegistrarLargadaForm, RegistrarChegadaForm
from django.shortcuts import get_object_or_404

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
        form = RegistrarLargadaForm(request.POST)
        if form.is_valid():
            numero_piloto = form.cleaned_data['numero_piloto']
            piloto = get_object_or_404(Piloto, numero_piloto=numero_piloto)
            agora = datetime.now().strftime('%H:%M:%S')
            largada= RegistrarLargada(numero_piloto=piloto, horario_largada= agora )
            largada.save()
            messages.success(request, 'Horário de largada cadastrado com sucesso')
            return redirect('registrar_largada')
    else:        
        form = RegistrarLargadaForm()

    return render(request, 'registrar_largada.html', {'form': form})


def registrar_chegada(request):
    numero_piloto = None
    if request.method == 'POST':
        form = RegistrarChegadaForm(request.POST)
        if form.is_valid():
            numero_piloto = form.cleaned_data['numero_piloto']
            piloto = get_object_or_404(Piloto, numero_piloto=numero_piloto)
            agora = datetime.now().strftime('%H:%M:%S')
            chegada = RegistrarChegada(numero_piloto=piloto, horario_chegada=agora)
            chegada.save()
            messages.success(request, 'Horário de chegada cadastrado com sucesso')

            piloto = Piloto.objects.get(numero_piloto=numero_piloto)
            largada = RegistrarLargada.objects.last()
            save_resultados(piloto, largada, chegada)

            return redirect('registrar_chegada')

    else:
        form = RegistrarChegadaForm()

    return render(request, 'registrar_chegada.html', {'form': form})


def save_resultados(piloto, largada, chegada):
    largada = RegistrarLargada.objects.filter(numero_piloto=largada.numero_piloto_id, horario_largada=largada.horario_largada).last()
    chegada = RegistrarChegada.objects.filter(numero_piloto=chegada.numero_piloto, horario_chegada=chegada.horario_chegada).last()
    piloto = Piloto.objects.get(nome=piloto.nome, numero_piloto=piloto.numero_piloto, moto=piloto.moto, categoria=piloto.categoria)
    nome = piloto.nome
    numero_piloto = piloto.numero_piloto
    moto = piloto.moto
    categoria = piloto.categoria
    id_volta = largada.id_volta
    horario_largada = largada.horario_largada
    horario_chegada = chegada.horario_chegada
    tempo_volta = datetime.combine(date.today(), horario_chegada) - datetime.combine(date.today(), horario_largada)

    resultado = Resultados(nome=nome, numero_piloto=numero_piloto, moto=moto, categoria=categoria,
                               id_volta=id_volta, horario_largada=horario_largada,
                               horario_chegada=horario_chegada, tempo_volta=tempo_volta)
   
    resultado.tempo_volta = tempo_volta
    resultado.tempo_total = sum(Resultados.objects.filter(numero_piloto=numero_piloto).values_list('tempo_volta', flat=True), tempo_volta)
    resultado.save()


        
def exibir_pilotos(request):
    nome = request.GET.get('nome')
    numero_piloto = request.GET.get('numero_piloto')
    categoria = request.GET.get('categoria')
    if nome and numero_piloto and categoria:
        pilotos = Piloto.objects.filter(nome=nome, numero_piloto=numero_piloto, categoria=categoria)
    else:
        pilotos = Piloto.objects.all()
    return render(request, 'exibir_pilotos.html', {'pilotos': pilotos})



def resultados(request):
    resultados = Resultados.objects.all()

    # Resultados gerais
    resultados_gerais = []
    for piloto in Piloto.objects.all():
        tempo_total = sum(resultado.tempo_volta.total_seconds() for resultado in resultados.filter(numero_piloto=piloto.numero_piloto))
        resultados_gerais.append({'piloto': piloto, 'numero_piloto': piloto.numero_piloto, 'tempo_total': tempo_total})
    resultados_gerais = sorted(resultados_gerais, key=lambda x: x['tempo_total'])

    # Resultados por categoria
    categorias = ['Over_50', 'Over_40', 'pro']
    resultados_por_categoria = {categoria: [] for categoria in categorias}
    resultados_dict = {categoria: resultados.filter(categoria=categoria) for categoria in categorias}

    tempo_total_por_piloto = {}
    for categoria, resultados_categoria in resultados_dict.items():
        for resultado in resultados_categoria:
            if resultado.nome not in [res['nome'] for res in resultados_por_categoria[categoria]] and resultado.numero_piloto not in [res['numero_piloto'] for res in resultados_por_categoria[categoria]]:
                if resultado.numero_piloto not in tempo_total_por_piloto:
                    tempo_total_por_piloto[resultado.numero_piloto] = sum(res.tempo_volta.total_seconds() for res in resultados_dict[categoria].filter(numero_piloto=resultado.numero_piloto))
                resultados_por_categoria[categoria].append({'nome': resultado.nome, 'numero_piloto': resultado.numero_piloto, 'tempo_total': tempo_total})

        resultados_por_categoria[categoria] = sorted(resultados_por_categoria[categoria], key=lambda x: x['tempo_total'])

    return render(request, 'resultados.html', {'resultados_gerais': resultados_gerais,
                                                'resultados_por_categoria': resultados_por_categoria})