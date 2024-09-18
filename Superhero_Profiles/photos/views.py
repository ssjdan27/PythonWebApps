from pathlib import Path
from django.views.generic import TemplateView

# Dictionary to hold superhero data
heroes = {
    'batman': {
        'name': 'Batman',
        'strengths': 'Intelligence, martial arts, gadgets',
        'weaknesses': 'Human limitations',
        'image': 'batman.jpg'
    },
    'deadpool': {
        'name': 'Deadpool',
        'strengths': 'Regeneration, martial arts, marksmanship',
        'weaknesses': 'Mental instability',
        'image': 'deadpool.jpg'
    },
    'robin': {
        'name': 'Robin',
        'strengths': 'Agility, martial arts, detective skills',
        'weaknesses': 'Human limitations',
        'image': 'robin.jpg'
    },
    'spiderman': {
        'name': 'Spiderman',
        'strengths': 'Super strength, agility, spider-sense, web-shooting',
        'weaknesses': 'Ethyl chloride pesticide',
        'image': 'spiderman.jpg'
    },
    'wolverine': {
        'name': 'Wolverine',
        'strengths': 'Regeneration, adamantium skeleton, martial arts',
        'weaknesses': 'Adamantium poisoning, rage',
        'image': 'wolverine.jpg'
    }
}

# Function to return a list of photos from the static images folder
def photo_list():
    def photo_details(hero_name):
        return dict(file=f'{hero_name}.jpg', caption=f'{hero_name.capitalize()} Photo')

    return [photo_details(hero) for hero in heroes]

# View for the hero list (index page)
class HeroListView(TemplateView):
    template_name = 'heroes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heroes'] = heroes
        context['photos'] = photo_list()
        return context

# View for individual hero detail
class HeroDetailView(TemplateView):
    template_name = 'hero.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hero_id = kwargs.get('hero_id')  # Get hero name from URL
        hero_data = heroes.get(hero_id)
        
        if hero_data:
            context['hero'] = hero_data
            context['photo'] = dict(file=f"{hero_data['image']}", caption=f"{hero_data['name']} Photo")
        return context
