from django.views.generic import CreateView, ListView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .models import Photo

class PhotoCreateView(CreateView):
    model = Photo
    fields = ['title', 'image']
    template_name = "photo/photo_add.html"
    success_url = reverse_lazy('photo_list')

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)

class PhotoListView(ListView):
    model = Photo
    template_name = "photo/photo_list.html"
    context_object_name = "photos"

class PhotoDeleteView(DeleteView):
    model = Photo
    template_name = "photo/photo_delete.html"
    success_url = reverse_lazy('photo_list')

class PhotoCarouselView(TemplateView):
    template_name = 'photo/photo_carousel.html'

    def get_context_data(self, **kwargs):
        photos = Photo.objects.all()
        return {'carousel': self.carousel_data(photos)}

    def carousel_data(self, photos):
        return [
            {
                'image_url': photo.image.url,
                'id': idx,
                'active': 'active' if idx == 0 else '',
                'aria': 'aria-current="true"' if idx == 0 else '',
                'label': f"Photo {photo.title}"
            }
            for idx, photo in enumerate(photos)
        ]