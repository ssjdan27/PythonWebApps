from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Superhero

def index(request):
    return render(request, 'hero/index.html')

class SuperheroListView(ListView):
    model = Superhero
    template_name = 'hero/superhero_list.html'
    context_object_name = 'superheroes'

class SuperheroDetailView(DetailView):
    model = Superhero
    template_name = 'hero/superhero_detail.html'

class SuperheroCreateView(CreateView):
    model = Superhero
    template_name = 'hero/superhero_form.html'
    fields = ['name', 'identity', 'description', 'strength', 'weakness', 'image']
    success_url = reverse_lazy('superhero_list')
    extra_context = {'title': 'Add New Superhero'}

class SuperheroUpdateView(UpdateView):
    model = Superhero
    template_name = 'hero/superhero_form.html'
    fields = ['name', 'identity', 'description', 'strength', 'weakness', 'image']
    success_url = reverse_lazy('superhero_list')
    extra_context = {'title': 'Edit Superhero'}

class SuperheroDeleteView(DeleteView):
    model = Superhero
    template_name = 'hero/superhero_confirm_delete.html'
    success_url = reverse_lazy('superhero_list')