from django.shortcuts import render, redirect
from crono.models import Piloto, RegistrarLargada, RegistrarChegada,Resultados, DadosCorrida
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta, timezone, date
from crono.forms import RegistrarLargadaForm, RegistrarChegadaForm, CadastrarPilotoForm
from django.shortcuts import get_object_or_404

def cadastrar_piloto(request):
    if request.method == 'POST':
        form = CadastrarPilotoForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            numero_piloto = form.cleaned_data['numero_piloto']
            moto = form.cleaned_data['moto']
            categoria = form.cleaned_data['categoria']
        
        # Verifica se já existe um piloto com o mesmo nome ou número
            if Piloto.objects.filter(Q(nome=nome) | Q(numero_piloto=numero_piloto)).exists():
                messages.error(request, 'Já existe um piloto com esse nome ou número.')
            else:
                piloto = Piloto(nome=nome, numero_piloto=numero_piloto, moto=moto, categoria=categoria)
                piloto.save()
                messages.success(request, 'Piloto cadastrado com sucesso.')
                return redirect('cadastrar_piloto')
            
    else:
        form = CadastrarPilotoForm()

    return render(request, 'cadastrar_piloto.html', {'form': form})


def registrar_largada(request):
    if request.method == 'POST':
        form = RegistrarLargadaForm(request.POST)
        if form.is_valid():
            numero_piloto = form.cleaned_data['numero_piloto']
            piloto = get_object_or_404(Piloto, numero_piloto=numero_piloto)
            agora = datetime.now().strftime('%H:%M:%S.%f')[:-3]
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
            agora = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            chegada = RegistrarChegada(numero_piloto=piloto, horario_chegada=agora)
            chegada.save()

            
           
            messages.success(request, 'Horário de chegada cadastrado com sucesso')

            # Atualiza dados class Resultados
            chegada_agora_time = datetime.strptime(agora, '%H:%M:%S.%f').time()
            largada_resultado = RegistrarLargada.objects.filter(numero_piloto=piloto).last()
            horario_largada_resultado = largada_resultado.horario_largada
            if largada_resultado:
                horario_largada_resultado = largada_resultado.horario_largada
            else:
                horario_largada_resultado = None
           
            tempo_volta = datetime.combine(date.today(), chegada_agora_time) - datetime.combine(date.today(), horario_largada_resultado)
            

            piloto = Piloto.objects.get(nome=piloto.nome, numero_piloto=piloto.numero_piloto, moto=piloto.moto, categoria=piloto.categoria)
            nome = piloto.nome
            numero_piloto = piloto.numero_piloto
            moto = piloto.moto
            categoria = piloto.categoria

            resultado = Resultados(nome=nome, numero_piloto=numero_piloto, moto=moto, categoria=categoria,
                               id_volta=largada_resultado.id_volta, horario_largada=horario_largada_resultado,
                               horario_chegada=chegada_agora_time, tempo_volta=tempo_volta)
   
            resultado.tempo_volta = tempo_volta
            resultado.tempo_total = sum(Resultados.objects.filter(numero_piloto=numero_piloto).values_list('tempo_volta', flat=True), tempo_volta)
            resultado.save()


           
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
    resultado =Resultados.objects.all()

    #resultados gerais
    resultados_gerais = []
    for piloto in Piloto.objects.all():
        tempo_total = sum(resultado.tempo_volta.total_seconds() for resultado in resultado.filter(numero_piloto=piloto.numero_piloto))
        tempo_total_str = '{:02d}:{:02d}:{:02.3f}'.format(int(tempo_total // 3600), int((tempo_total % 3600) // 60), (tempo_total % 60))
        
        if tempo_total_str != "00:00:0.000":
           resultados_gerais.append({'piloto': piloto, 'numero_piloto': piloto.numero_piloto, 'tempo_total': tempo_total_str})
        
    resultados_gerais = sorted(resultados_gerais, key=lambda x: x['tempo_total'])

    # Adicionando posição aos resultados gerais
    for position, piloto in enumerate(resultados_gerais, start=1):
        piloto['position'] = position

    # Resultados por categoria
    categorias = ['Over_50', 'Over_40', 'pro']
    resultados_por_categoria = {categoria: [] for categoria in categorias}
    resultados_dict = {categoria: resultado.filter(categoria=categoria) for categoria in categorias}

    tempo_total_por_piloto = {}
    for categoria, resultados_categoria in resultados_dict.items():
        for resultado in resultados_categoria:
            if resultado.nome not in [res['nome'] for res in resultados_por_categoria[categoria]] and resultado.numero_piloto not in [res['numero_piloto'] for res in resultados_por_categoria[categoria]]:
                if resultado.numero_piloto not in tempo_total_por_piloto:
                    tempo_total_por_piloto[resultado.numero_piloto] = sum(res.tempo_volta.total_seconds() for res in resultados_dict[categoria].filter(numero_piloto=resultado.numero_piloto))
                    tempo_total_por_piloto_str = '{:02d}:{:02d}:{:02.3f}'.format(int(tempo_total_por_piloto[resultado.numero_piloto] // 3600), 
                                                                            int((tempo_total_por_piloto[resultado.numero_piloto] % 3600) // 60),
                                                                            tempo_total_por_piloto[resultado.numero_piloto] % 60)
                    resultados_por_categoria[categoria].append({'nome': resultado.nome, 'numero_piloto': resultado.numero_piloto, 'tempo_total': tempo_total_por_piloto_str})

        resultados_por_categoria[categoria] = sorted(resultados_por_categoria[categoria], key=lambda x: x['tempo_total'])

    # Adicionando posição aos resultados por categoria
    for categoria, resultados_categoria in resultados_por_categoria.items():
        for position, resultado in enumerate(resultados_categoria, start=1):
            resultado['position'] = position

    return render(request, 'resultados.html', {'resultados_gerais': resultados_gerais,
                                                'resultados_por_categoria': resultados_por_categoria})



def resultado_piloto(request):
    piloto_detail = []
    for piloto in Piloto.objects.all():
        resultados = Resultados.objects.filter(numero_piloto=piloto.numero_piloto)
        volta_detail = []
        for resultado in resultados:
            tempo_volta = resultado.tempo_volta.total_seconds()
            tempo_volta_str = '{:02d}:{:02d}:{:02.3f}'.format(int(tempo_volta // 3600), int((tempo_volta % 3600) // 60), (tempo_volta % 60))
            horario_chegada_str = resultado.horario_chegada.strftime('%H:%M:%S')
            horario_largada_str = resultado.horario_largada.strftime('%H:%M:%S')
            volta_detail.append({
                'id_volta': resultado.id_volta,
                'horario_largada': horario_largada_str,
                'horario_chegada': horario_chegada_str,
                'tempo_volta': tempo_volta_str,
            })

        tempo_total = sum(resultado.tempo_volta.total_seconds() for resultado in resultados)
        tempo_total_str = '{:02d}:{:02d}:{:03.3f}'.format(int(tempo_total // 3600), int((tempo_total % 3600) // 60), (tempo_total % 60))

        piloto_detail.append({
            'piloto': piloto,
            'numero_piloto': piloto.numero_piloto,
            'voltas': volta_detail,
            'tempo_total': tempo_total_str,
        })

    return render(request, 'resultado_piloto.html', {'piloto_detail' : piloto_detail})



from django.db.models import Max, F
from crono.models import RegistrarLargada, RegistrarChegada, DadosCorrida

