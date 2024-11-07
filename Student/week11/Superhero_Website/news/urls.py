
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from .views_author import UserUpdateView, AuthorAddView
from .views_author import AuthorDetailView, AuthorHomeView, AuthorListView, AuthorUpdateView, AuthorDeleteView
from .views_article import ArticleDeleteView, ArticleDetailView, ArticleListView, ArticleCreateView, ArticleUpdateView
from .views_hero import SuperheroListView, SuperheroCreateView, SuperheroDetailView, SuperheroUpdateView, SuperheroDeleteView
from .views_investigator import InvestigatorDetailView, InvestigatorUpdateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/',            AuthorAddView.as_view(),    name='signup'),
    path('accounts/<int:pk>/',          UserUpdateView.as_view(),  name='user_edit'),
    path('',                            RedirectView.as_view(url='author/home')),
    path('author/',                     AuthorListView.as_view(),    name='author_list'),
    path('author/home',                 AuthorHomeView.as_view(),    name='author_home'),
    path('author/<int:pk>',             AuthorDetailView.as_view(),  name='author_detail'),
    path('author/add/',                 AuthorAddView.as_view(),     name='author_add'),
    path('author/<int:pk>/',            AuthorUpdateView.as_view(),  name='author_edit'),
    path('author/<int:pk>/delete',      AuthorDeleteView.as_view(),  name='author_delete'),
    path('article/',                    ArticleListView.as_view(),    name='article_list'),
    path('article/<int:pk>',            ArticleDetailView.as_view(),  name='article_detail'),
    path('article/add',                 ArticleCreateView.as_view(),  name='article_add'),
    path('article/<int:pk>/',           ArticleUpdateView.as_view(),  name='article_edit'),
    path('article/<int:pk>/delete',     ArticleDeleteView.as_view(),  name='article_delete'),
    path('hero/',                   SuperheroListView.as_view(), name='superhero_list'),
    path('hero/add/',               SuperheroCreateView.as_view(), name='superhero_add'),
    path('hero/<int:pk>/',          SuperheroDetailView.as_view(), name='superhero_detail'),
    path('hero/<int:pk>/edit/',     SuperheroUpdateView.as_view(), name='superhero_edit'),
    path('hero/<int:pk>/delete/',   SuperheroDeleteView.as_view(), name='superhero_delete'),
    path('investigator/<int:pk>/', InvestigatorDetailView.as_view(), name='investigator_detail'),
    path('investigator/edit/', InvestigatorUpdateView.as_view(), name='investigator_edit'),
]
