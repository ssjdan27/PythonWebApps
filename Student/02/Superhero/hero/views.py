from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'heroes.html'


class HulkView(TemplateView):
    template_name = 'hero.html'

    def get_context_data(self, **kwargs):
        return {
            'title': 'Hulk',
            'body': 'My name is Bruce Banner. Yippie.',
            'image': '/static/images/hulk.jpg'
        }


class IronManView(TemplateView):
    template_name = "hero.html"

    def get_context_data(self, **kwargs):
        return {
            'title': 'Iron Man',
            'body': 'My name is Tony Stark, but I am Iron Man. Iron Man is alright.',
            'image': '/static/images/iron_man.jpg'
        }


class BlackWidowView(TemplateView):
    template_name = 'hero.html'

    def get_context_data(self, **kwargs):
        return {
            'title': 'Black Widow',
            'body': 'My name is Natasha Romanova. I do not know much about Black Widow.',
            'image': '/static/images/black_widow.jpg'
        }
        
class SpiderManView(TemplateView):
    template_name = "hero.html"

    def get_context_data(self, **kwargs):
        return {
            'title': 'Spiderman',
            'body': 'Spiderman is the best',
            'image': '/static/images/spiderman.jpeg'
        }