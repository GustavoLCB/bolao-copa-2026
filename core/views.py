from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.contrib.auth import login
from .forms import RegistroForm
from .models import Partida, Palpite

@login_required 
def home(request):
    partidas = Partida.objects.all().order_by('data_hora', 'grupo_fase')
    meus_palpites = Palpite.objects.filter(usuario=request.user)
    dicionario_palpites = {palpite.partida.id: palpite for palpite in meus_palpites}
    
    agora = timezone.now()
    
    for jogo in partidas:
        jogo.meu_palpite = dicionario_palpites.get(jogo.id)
        jogo.ja_comecou = jogo.data_hora <= agora
        
    return render(request, 'home.html', {'partidas': partidas})

@login_required
def dar_palpite(request, partida_id):
    partida = get_object_or_404(Partida, id=partida_id)
    
    if partida.data_hora <= timezone.now():
        return redirect('home')
        
    palpite_existente = Palpite.objects.filter(usuario=request.user, partida=partida).first()

    if request.method == 'POST':
        gols_m = request.POST.get('gols_mandante')
        gols_v = request.POST.get('gols_visitante')

        if palpite_existente:
            palpite_existente.gols_mandante = gols_m
            palpite_existente.gols_visitante = gols_v
            palpite_existente.save()
        else:
            Palpite.objects.create(
                usuario=request.user,
                partida=partida,
                gols_mandante=gols_m,
                gols_visitante=gols_v
            )
        return redirect('home')

    return render(request, 'palpite.html', {
        'partida': partida, 
        'palpite_existente': palpite_existente
    })

@login_required
def ranking(request):
    usuarios = User.objects.annotate(
        total_pontos=Coalesce(Sum('palpite__pontos'), 0)
    ).order_by('-total_pontos')
    
    return render(request, 'ranking.html', {'usuarios': usuarios})

def registrar(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistroForm()
        
    return render(request, 'registration/registrar.html', {'form': form})

@login_required
def regras(request):
    return render(request, 'regras.html')