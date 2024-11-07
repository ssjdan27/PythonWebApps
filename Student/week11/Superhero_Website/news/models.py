from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy


class Author(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    bio = models.TextField()

    def __str__(self):
        return f'{self.user.username}'

    def get_absolute_url(self):
        return reverse_lazy('author_detail', args=[str(self.id)])

    @property
    def name(self):
        return self.user.first_name + ' ' + self.user.last_name

    @property
    def articles(self):
        return Article.objects.filter(author=self)

    @staticmethod
    def get_me(user):
        return Author.objects.get_or_create(user=user)[0]


class Article (models.Model):

    author = models.ForeignKey(Author, on_delete=models.CASCADE, editable=False)
    title = models.CharField(max_length=100)
    body = models.TextField()

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse_lazy('article_detail', args=[str(self.id)])

class Superhero(models.Model):
    name = models.CharField(max_length=200)
    identity = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    strength = models.CharField(max_length=100, default='')
    weakness = models.CharField(max_length=100, default='')
    image = models.CharField(max_length=100, default='')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='superheroes')
    
    def __str__(self):
        return self.name
    
class Investigator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name