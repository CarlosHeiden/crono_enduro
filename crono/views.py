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

            save_resultados(agora, numero_piloto)


           
            return redirect('registrar_chegada')

    else:
        form = RegistrarChegadaForm()

    return render(request, 'registrar_chegada.html', {'form': form})



def save_resultados(agora, numero_piloto):
    chegada_agora_time = datetime.strptime(agora, '%H:%M:%S.%f').time()
    piloto = get_object_or_404(Piloto, numero_piloto=numero_piloto)
    #chegada_agora_time = RegistrarChegada.objects.filter(numero_piloto=piloto).last()
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

    dados_corrida = DadosCorrida(nome=nome, numero_piloto=numero_piloto, moto=moto, categoria=categoria,
                        id_volta=largada_resultado.id_volta, horario_largada=horario_largada_resultado,
                        horario_chegada=chegada_agora_time, tempo_volta=tempo_volta)

    #resultado.tempo_volta = tempo_volta
    #resultado.tempo_total = sum(Resultados.objects.filter(numero_piloto=numero_piloto).values_list('tempo_volta', flat=True), tempo_volta)
    dados_corrida.save()





        
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
        print(resultados_por_categoria)
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


def resultado_tomada_tempo(request):
    resultado_geral_tomada_tempo = []
    for piloto in Piloto.objects.all():
        tempo_volta_min = None
        for resultado in DadosCorrida.objects.filter(numero_piloto=piloto.numero_piloto):
            tempo_volta = resultado.tempo_volta.total_seconds()
            if tempo_volta_min is None or tempo_volta < tempo_volta_min:
                tempo_volta_min = tempo_volta
        if tempo_volta_min is not None:
            horas = int(tempo_volta_min // 3600)
            minutos = int((tempo_volta_min % 3600) // 60)
            segundos = int(tempo_volta_min % 60)
            milissegundos = int((tempo_volta_min % 1) * 1000)

            # Formate cada parte do tempo com zeros à esquerda, se necessário
            tempo_volta_min = '{:02d}:{:02d}:{:02d}.{:03d}'.format(horas, minutos, segundos, milissegundos)


            resultado_geral_tomada_tempo.append({
                'piloto': piloto,
                'numero_piloto': piloto.numero_piloto,
                'tempo_volta': tempo_volta_min,
            })
    resultado_geral_tomada_tempo = sorted(resultado_geral_tomada_tempo, key=lambda x: x['tempo_volta'])

    # Adicionando posição aos resultados gerais
    for position, piloto in enumerate(resultado_geral_tomada_tempo, start=1):
        piloto['position'] = position

    return render(request, 'resultado_geral_tomada_tempo.html', {'resultado_geral_tomada_tempo': resultado_geral_tomada_tempo})

from django.db.models import Min

from django.db.models import Min

from django.db.models import Min

def resultado_tomada_tempo_por_categorias(request):
    categorias = ['Over_50', 'Over_40', 'pro']
    resultados_por_categoria_over_50 = []
    resultados_por_categoria_over_40 = []
    resultados_por_categoria_pro = []

    for categoria in categorias:
        resultados_categoria = DadosCorrida.objects.filter(categoria=categoria)

        # Usamos a função annotate com Min para encontrar o menor tempo de volta para cada piloto
        resultados_categoria = resultados_categoria.values('nome','numero_piloto').annotate(min_tempo=Min('tempo_volta')).order_by('min_tempo')

        for resultado in resultados_categoria:
            tempo_volta_min = resultado['min_tempo']
            segundos_totais = tempo_volta_min.total_seconds()

            horas = int(segundos_totais // 3600)
            minutos = int((segundos_totais % 3600) // 60)
            segundos = int(segundos_totais % 60)
            milissegundos = int((segundos_totais - int(segundos_totais)) * 1000)

            # Formate cada parte do tempo com zeros à esquerda, se necessário
            tempo_volta_formatado = '{:02d}:{:02d}:{:02d}.{:03d}'.format(horas, minutos, segundos, milissegundos)

            if categoria == 'Over_50':
                resultados_por_categoria_over_50.append({
                    'nome': resultado['nome'],
                    'numero_piloto': resultado['numero_piloto'],
                    'tempo_total': tempo_volta_formatado
                })
            elif categoria == 'Over_40':
                resultados_por_categoria_over_40.append({
                    'nome': resultado['nome'],
                    'numero_piloto': resultado['numero_piloto'],
                    'tempo_total': tempo_volta_formatado
                })
            elif categoria == 'pro':
                resultados_por_categoria_pro.append({
                    'nome': resultado['nome'],
                    'numero_piloto': resultado['numero_piloto'],
                    'tempo_total': tempo_volta_formatado
                })

    return render(request, 'resultado_tomada_tempo_por_categorias.html', {
        'resultados_por_categoria_over_50': resultados_por_categoria_over_50,
        'resultados_por_categoria_over_40': resultados_por_categoria_over_40,
        'resultados_por_categoria_pro': resultados_por_categoria_pro
    })
