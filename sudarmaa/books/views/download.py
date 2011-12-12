from django.views.generic import DetailView
from django.views.generic.detail import BaseDetailView
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
        sections = []
        for chapter in self.object.top_pages():
            section = ez_epub.Section()
            section.title = chapter.title
            section.text.append(b2h(chapter.content))
            sections.append(section)
        book.sections = sections
        filename = self.temp_filename.format(self.object.id)
        book.make(filename)
        return sendfile(request, filename + '.epub')

