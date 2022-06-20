
from django.urls import path

from .views_author import AuthorDetailView, AuthorHomeView, AuthorListView, AuthorUpdateView, AuthorDeleteView


urlpatterns = [

    # Author
    path('',                    AuthorListView.as_view(),    name='author_list'),
    path('home',                AuthorHomeView.as_view(),    name='author_home'),
    path('<int:pk>',            AuthorDetailView.as_view(),  name='author_detail'),
    # path('add',               AuthorCreateView.as_view(),  name='author_add'),
    path('<int:pk>/',           AuthorUpdateView.as_view(),  name='author_edit'),
    path('<int:pk>/delete',     AuthorDeleteView.as_view(),  name='author_delete'),

]
