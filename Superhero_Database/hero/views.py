from django.views.generic import ListView, DetailView
from .models import Superhero

class HeroListView(ListView):
    model = Superhero
    template_name = 'heroes.html'  # Template for the list view
    context_object_name = 'object_list'  # Ensures the superheroes are accessible in the template


class HeroDetailView(DetailView):
    model = Superhero
    template_name = 'hero.html'  # Template for the detail view

    def get_object(self):
        # Fetch superhero by name from the URL
        return Superhero.objects.get(name=self.kwargs['name'])
