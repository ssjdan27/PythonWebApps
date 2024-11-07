from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, RedirectView, UpdateView

from .models import Article, Investigator


def list_articles(investigator):
    return dict(articles=Article.objects.filter(investigator=investigator))


def get_investigator(user):
    return Investigator.objects.get_or_create(user=user)[0]


class InvestigatorHomeView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_anonymous:
            return '/article/'
        return f'/investigator/{get_investigator(self.request.user).pk}'


class InvestigatorListView(ListView):
    template_name = 'investigator_list.html'
    model = Investigator

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        return kwargs


class InvestigatorDetailView(DetailView):
    template_name = 'investigator_detail.html'
    model = Investigator

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update(list_articles(kwargs.get('object')))
        return kwargs

class InvestigatorAddView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/account_add.html'

class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "registration/account_edit.html"
    model = User
    fields = ['first_name', 'last_name', 'username', 'email']
    success_url = reverse_lazy('investigator_home')


class InvestigatorUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "investigator_edit.html"
    model = Investigator
    fields = '__all__'


class InvestigatorDeleteView(LoginRequiredMixin, DeleteView):
    model = Investigator
    template_name = 'investigator_delete.html'
    success_url = reverse_lazy('investigator_list')
