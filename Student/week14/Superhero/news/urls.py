
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from .views_investigator import UserUpdateView, InvestigatorAddView
from .views_investigator import InvestigatorDetailView, InvestigatorHomeView, InvestigatorListView, InvestigatorUpdateView, InvestigatorDeleteView
from .views_article import ArticleDeleteView, ArticleDetailView, ArticleListView, ArticleCreateView, ArticleUpdateView
from .views_hero import SuperheroListView, SuperheroCreateView, SuperheroDetailView, SuperheroUpdateView, SuperheroDeleteView
from .views_photos import PhotoListView, PhotoCreateView, PhotoDeleteView, PhotoCarouselView
from .views_messages import MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Accounts
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/',            InvestigatorAddView.as_view(),    name='signup'),
    path('accounts/<int:pk>/',          UserUpdateView.as_view(),  name='user_edit'),

    # Investigator
    path('',                            RedirectView.as_view(url='investigator/home')),
    path('investigator/',                     InvestigatorListView.as_view(),    name='investigator_list'),
    path('investigator/home',                 InvestigatorHomeView.as_view(),    name='investigator_home'),
    path('investigator/<int:pk>',             InvestigatorDetailView.as_view(),  name='investigator_detail'),
    path('investigator/add/',                 InvestigatorAddView.as_view(),     name='investigator_add'),
    path('investigator/<int:pk>/',            InvestigatorUpdateView.as_view(),  name='investigator_edit'),
    path('investigator/<int:pk>/delete',      InvestigatorDeleteView.as_view(),  name='investigator_delete'),

    # Article
    path('article/',                    ArticleListView.as_view(),    name='article_list'),
    path('article/<int:pk>',            ArticleDetailView.as_view(),  name='article_detail'),
    path('article/add',                 ArticleCreateView.as_view(),  name='article_add'),
    path('article/<int:pk>/',           ArticleUpdateView.as_view(),  name='article_edit'),
    path('article/<int:pk>/delete',     ArticleDeleteView.as_view(),  name='article_delete'),

    # Superhero
    path('hero/',                   SuperheroListView.as_view(), name='superhero_list'),
    path('hero/add/',               SuperheroCreateView.as_view(), name='superhero_add'),
    path('hero/<int:pk>/',          SuperheroDetailView.as_view(), name='superhero_detail'),
    path('hero/<int:pk>/edit/',     SuperheroUpdateView.as_view(), name='superhero_edit'),
    path('hero/<int:pk>/delete/',   SuperheroDeleteView.as_view(), name='superhero_delete'),

    # Photos
    path('photo/', PhotoListView.as_view(), name='photo_list'),
    path('photo/add/', PhotoCreateView.as_view(), name='photo_add'),
    path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name='photo_delete'),
    path('photo/carousel/', PhotoCarouselView.as_view(), name='photo_carousel'),
    
    # Messages
    path('message/', MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>', MessageDetailView.as_view(), name='message_detail'),
    path('message/add', MessageCreateView.as_view(), name='message_add'),
    path('message/<int:pk>/', MessageUpdateView.as_view(), name='message_edit'),
    path('message/<int:pk>/delete', MessageDeleteView.as_view(), name='message_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
