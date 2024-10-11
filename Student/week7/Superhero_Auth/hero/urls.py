from django.urls import path
from django.contrib import admin
from django.urls import include
from hero.views import SignUpView
from .views import (
    SuperheroListView,
    SuperheroDetailView,
    SuperheroCreateView,
    SuperheroUpdateView,
    SuperheroDeleteView,
)

urlpatterns = [
    path('', SuperheroListView.as_view(), name='superhero_list'),
    path('hero/add/', SuperheroCreateView.as_view(), name='superhero_add'),
    path('hero/<int:pk>/', SuperheroDetailView.as_view(), name='superhero_detail'),
    path('hero/<int:pk>/edit/', SuperheroUpdateView.as_view(), name='superhero_edit'),
    path('hero/<int:pk>/delete/', SuperheroDeleteView.as_view(), name='superhero_delete'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
]
