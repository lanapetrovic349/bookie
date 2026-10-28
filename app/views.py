from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import Count
from django.db.models.functions import Lower
from django.shortcuts import render, redirect

from app.models import AppQuiz, AppMembership


# Create your views here.

def login1(request):
    if request.user.is_authenticated:
        return redirect('svikvizovi')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('svikvizovi')
    else:
        form = AuthenticationForm()
    return render(request, 'index.html', {'form': form})

def logout1(request):
    logout(request)
    return redirect('login1')

@login_required
def svikvizovi(request):
    kvizovi = AppQuiz.objects.all()
    context = {'kvizovi': kvizovi}
    return render(request, 'svi_kvizovi.html', context)

def register1(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login1')
        else:
            print(form.non_field_errors)
    context = {'form': form}
    return render(request, 'registracija.html', context)


@login_required
def prikaziKviz(request, kvizId):
    kviz = AppQuiz.objects.get(id=kvizId)
    timovi = kviz.teams.all()
    return render(request, "detalji_kviza.html", {"kviz": kviz, "timovi": timovi})

def sviTimoviKviza(request, kvizId):
    return prikaziKviz(request, kvizId)

@login_required
def top_kvizovi(request):
    rezultati = []

    for kviz in AppQuiz.objects.all():
        clanstva = AppMembership.objects.filter(quiz=kviz).values_list('user_id', flat=True)
        jedinstveni_useri = set(clanstva)
        broj_ucesnika = len(jedinstveni_useri)

        rezultati.append((kviz, broj_ucesnika))

    rezultati = sorted(
        rezultati,
        key=lambda x: (-x[1], x[0].title)
    )

    top3 = rezultati[:3]

    top_kvizovi = [
        {"title": kviz.title, "count": count}
        for kviz, count in top3
    ]

    return render(request, "top_kviz.html", {"top_kvizovi": top_kvizovi})

