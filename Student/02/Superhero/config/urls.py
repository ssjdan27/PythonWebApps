from django.urls import path
from hero.views import BlackWidowView, HulkView, IndexView, IronManView, SpiderManView

urlpatterns = [
    path('', IndexView.as_view()),
    path('hulk', HulkView.as_view()),
    path('ironman', IronManView.as_view()),
    path('blackwidow', BlackWidowView.as_view()),
    path('spiderman', SpiderManView.as_view()),
]