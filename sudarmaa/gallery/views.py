# Create your views here.
from django.views.generic import ListView, CreateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from gallery.forms import PhotoForm

class ImageList(ListView):
    template_name = 'photo_list.html'
    
    def get_queryset(self):
        return self.request.user.photos.order_by('date_added')

    def get_context_data(self, *args, **kwargs):
        data = super(ImageList, self).get_context_data(*args, **kwargs)
        data['form'] = PhotoForm()
        return data

class UploadImage(CreateView):
    template_name = 'photo_list.html'
    form_class = PhotoForm

    def get_success_url(self):
        return reverse('choose-image')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        data = super(UploadImage, self).get_context_data(*args, **kwargs)
        data['object_list'] = self.request.user.photos.order_by('date_added')
        return data

