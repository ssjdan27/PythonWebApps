from django.views.generic import CreateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, RedirectView, UpdateView
from .models import Message

class MessageListView(ListView):
    model = Message
    template_name = 'messages/message_list.html'
    context_object_name = 'messages'

class MessageDetailView(DetailView):
    model = Message
    template_name = 'messages/message_detail.html'
    context_object_name = 'message'

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ['title', 'text']
    template_name = 'messages/message_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    success_url = reverse_lazy('message_list')

class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ['title', 'text']
    template_name = 'messages/message_form.html'
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    success_url = reverse_lazy('message_list')

class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'messages/message_confirm_delete.html'
    success_url = reverse_lazy('message_list')