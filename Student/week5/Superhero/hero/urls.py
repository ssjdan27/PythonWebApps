# hero/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.HeroListView, name='hero-list'),
    path('hero/<str:hero_name>/', views.HeroDetailView, name='hero-detail'),
]
