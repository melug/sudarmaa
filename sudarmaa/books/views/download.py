from django.views.generic import DetailView
from django.views.generic.detail import BaseDetailView
from django.conf import settings
from sendfile import sendfile

from books.models import Book

class DownloadPage(DetailView):

    def get_queryset(self):
        return Book.publish

    def get_template_names(self):
        return [ 'books/download_page.html' ]
    
class DownloadBook(BaseDetailView):
    model = Book

    def get(self, request, **kwargs):
        self.object = self.get_object() 
        context = self.get_context_data(object=self.object)
        return sendfile(request, self.object.get_epub_file())

