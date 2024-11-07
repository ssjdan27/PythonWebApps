from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Investigator

class InvestigatorDetailView(LoginRequiredMixin, DetailView):
    model = Investigator
    template_name = 'main/investigator_detail.html'

class InvestigatorUpdateView(LoginRequiredMixin, UpdateView):
    model = Investigator
    fields = ['name']
    template_name = 'main/investigator_form.html'
    success_url = reverse_lazy('index')

    def get_object(self):
        return self.request.user.investigator
