# hero/views.py

from django.shortcuts import render, get_object_or_404
from .models import Superhero

def HeroListView(request):
    heroes = Superhero.objects.all()
    return render(request, 'heroes.html', {'heroes': heroes})

def HeroDetailView(request, hero_name):
    hero = get_object_or_404(Superhero, name=hero_name)
    return render(request, 'hero.html', {'hero': hero})
