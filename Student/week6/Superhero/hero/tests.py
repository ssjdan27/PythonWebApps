from django.test import TestCase
from .models import Superhero

class SuperheroModelTest(TestCase):
    def setUp(self):
        Superhero.objects.create(
            name='Test Hero',
            identity='Test Identity',
            description='Test Description',
            strength='Test Strength',
            weakness='Test Weakness',
            image='test_image.jpg'
        )

    def test_superhero_creation(self):
        hero = Superhero.objects.get(name='Test Hero')
        self.assertEqual(hero.identity, 'Test Identity')
