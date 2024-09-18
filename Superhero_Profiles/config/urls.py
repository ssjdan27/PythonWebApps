from django.urls import path
from photos.views import HeroListView, HeroDetailView

urlpatterns = [
    path('', HeroListView.as_view(), name='hero-list'),  # For the hero list (index page)
    path('hero/<str:hero_id>/', HeroDetailView.as_view(), name='hero-detail'),  # For hero detail pages
]
