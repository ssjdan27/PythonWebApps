from django.views.generic import RedirectView
from django.urls import path

from photos.views import PhotoDetailView, PhotoListView


urlpatterns = [

    # Home
    path('', RedirectView.as_view(url='hero/')),

    # Photos
    path('hero/', PhotoListView.as_view()),
    path('hero/<int:id>', PhotoDetailView.as_view()),
]
