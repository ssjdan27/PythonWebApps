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


class ArticleView(RedirectView):
    url = reverse_lazy("article_list")


class ArticleListView(ListView):
    template_name = "article_list.html"
    model = Article


class ArticleDetailView(DetailView):
    template_name = "article_detail.html"
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        md = markdown.Markdown(extensions=["fenced_code"])
        markdown_content = self.object
        markdown_content.content = md.convert(markdown_content.body)
        context["markdown_content"] = markdown_content
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    template_name = "article_add.html"
    model = Article
    fields = "__all__"

    def form_valid(self, form):
        form.instance.investigator = get_investigator(self.request.user)
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "article_edit.html"
    model = Article
    fields = "__all__"


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy("article_list")
