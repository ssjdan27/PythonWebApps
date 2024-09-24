from django.urls import path
from . import views

urlpatterns = [
    path('', views.HeroListView.as_view(), name='hero_list'),  # The URL pattern for the list view
]