# Create your views here.
from django.views.generic import ListView, CreateView
from django.core.urlresolvers import reverse

from photologue.models import Gallery
from gallery.forms import PhotoForm

class ImageList(ListView):
    template_name = 'photo_list.html'
    
    def get_queryset(self):
        username = self.request.user.username
        gallery, created = Gallery.objects.get_or_create(title=username, title_slug=username)
        return gallery.photos.order_by('date_added')

    def get_context_data(self, *args, **kwargs):
        data = super(ImageList, self).get_context_data(*args, **kwargs)
        data['form'] = PhotoForm()
        return data

class UploadImage(CreateView):
    template_name = 'photo_list.html'
    form_class = PhotoForm

    def get_success_url(self):
        return reverse('choose-image')

    def get_context_data(self, *args, **kwargs):
        data = super(UploadImage, self).get_context_data(*args, **kwargs)
        data['object_list'] = []
        return data

