import re
import os

from django.views.generic import DetailView
from django.views.generic.detail import BaseDetailView
from django.conf import settings
from epub import ez_epub
from sendfile import sendfile

from books.models import Book
from books.templatetags.bbcode import bbcode2html

b2h = bbcode2html

class DownloadPage(DetailView):
    model = Book

    def get_template_names(self):
        return [ 'books/download_page.html' ]
    
class DownloadBook(BaseDetailView):
    model = Book
    temp_filename = '/tmp/epub/{0}'

    def get(self, request, **kwargs):
        self.object = self.get_object() 
        context = self.get_context_data(object=self.object)
        book = ez_epub.Book()
        book.title = self.object.title
        book.authors = [ '{0} {1}'.format(author.firstname, author.lastname) for author in book.authors ]
        if self.object.photo:
            photo_path = os.path.join(settings.MEDIA_ROOT,
                self.object.photo.image.name)
            print photo_path
            book.cover = photo_path
        sections = []
        for chapter in self.object.top_pages():
            section = ez_epub.Section()
            section.title = chapter.title
            for para in re.split('[\n\r]+', chapter.content):
                if para:
                    section.text.append(b2h(para))
            sections.append(section)
        book.sections = sections
        filename = self.temp_filename.format(self.object.id)
        book.make(filename)
        return sendfile(request, filename + '.epub')

