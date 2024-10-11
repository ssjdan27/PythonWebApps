from django.db import models
from django.contrib.auth.models import User

class Superhero(models.Model):
    name = models.CharField(max_length=100)
    identity = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    strength = models.CharField(max_length=100, default='')
    weakness = models.CharField(max_length=100, default='')
    image = models.CharField(max_length=100, default='')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='superheroes')

    def __str__(self):
        return self.name
