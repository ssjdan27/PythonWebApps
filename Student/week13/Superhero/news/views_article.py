import markdown
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django import forms
from django.forms.models import inlineformset_factory
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

# Inline Formset for associating photos with articles
PhotoFormSet = inlineformset_factory(
    Article, Photo, 
    fields=('title', 'image'), 
    extra=3,  # Allow up to 3 photos to be uploaded initially
    can_delete=True
)

# Optional: Define a base form for articles if needed
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body']

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
    fields = ['title', 'body']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['photo_formset'] = PhotoFormSet(self.request.POST, self.request.FILES)
        else:
            data['photo_formset'] = PhotoFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        photo_formset = context['photo_formset']
        form.instance.investigator = self.request.user.investigator  # Associate the article with the investigator

        if photo_formset.is_valid():
            self.object = form.save()  # Save the article
            photo_formset.instance = self.object  # Associate photos with the article

            # Assign the uploader to each photo in the formset
            photos = photo_formset.save(commit=False)
            for photo in photos:
                photo.uploaded_by = self.request.user  # Assign the uploader
                photo.save()  # Save each photo
            return super().form_valid(form)
        else:
            return self.form_invalid(form)



class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "article_edit.html"
    model = Article
    form_class = ArticleForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['photo_formset'] = PhotoFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['photo_formset'] = PhotoFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        photo_formset = context['photo_formset']
        if photo_formset.is_valid():
            self.object = form.save()
            photo_formset.instance = self.object
            photo_formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy('article_list')
