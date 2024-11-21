from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy


class Investigator(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    bio = models.TextField()
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.user.username}'

    def get_absolute_url(self):
        return reverse_lazy('investigator_detail', args=[str(self.id)])

    @property
    def name(self):
        return self.user.first_name + ' ' + self.user.last_name

    @property
    def articles(self):
        return Article.objects.filter(investigator=self)

    @staticmethod
    def get_me(user):
        return Investigator.objects.get_or_create(user=user)[0]


class Article (models.Model):

    investigator = models.ForeignKey(Investigator, on_delete=models.CASCADE, editable=False)
    title = models.CharField(max_length=100)
    body = models.TextField()
    image = models.ImageField(upload_to='articles/', blank=True, null=True)


    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse_lazy('article_detail', args=[str(self.id)])

def get_upload(instance, filename):
    return f'images/{filename}'

class Photo(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True, upload_to=get_upload)
    uploaded_by = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='photos'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='photos', null=True, blank=True
    )


class Superhero(models.Model):
    name = models.CharField(max_length=200)
    identity = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    strength = models.CharField(max_length=100, default='')
    weakness = models.CharField(max_length=100, default='')
    image = models.CharField(max_length=100, default='')
    investigator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='superheroes')
    photos = models.ManyToManyField(Photo, blank=True, related_name='superheroes')

    def add_photo(self, photo):
        self.photos.add(photo)
    
    def __str__(self):
        return self.name