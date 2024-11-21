import markdown
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    RedirectView,
    UpdateView,
)
from django.shortcuts import render

from .models import Article
from .views_investigator import get_investigator
from .models import Photo


class ArticleView(RedirectView):
    url = reverse_lazy("article_list")


class ArticleListView(ListView):
    template_name = "article_list.html"
    model = Article


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        md = markdown.Markdown(extensions=["fenced_code"])
        markdown_content = self.object
        markdown_content.body = md.convert(markdown_content.body)
        context["markdown_content"] = markdown_content.body

        # Fetch photos related to the article
        photos = Photo.objects.filter(article=self.object)
        print(f"Debug: Photos for article {self.object.pk}: {photos}")  # Debug statement
        context['carousel'] = self.carousel_data(photos)
        return context

    def carousel_data(self, photos):
        data = []
        for photo in photos:
            if photo.image:  # Ensure the photo has an image file
                print(f"Debug: Photo image URL = {photo.image.url}")  # Debug statement
                data.append({
                    'image_url': photo.image.url,
                    'article_title': self.object.title,
                })
        return data

class ArticleCreateView(LoginRequiredMixin, CreateView):
    template_name = "article_add.html"
    model = Article
    fields = ['title', 'body', 'image']  # Exclude 'investigator' from the form

    def form_valid(self, form):
        form.instance.investigator = self.request.user.investigator
        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "article_edit.html"
    model = Article
    fields = ['title', 'body', 'image']  # Exclude 'investigator' from the form

class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy('article_list')
