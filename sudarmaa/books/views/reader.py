from django.views.generic import DetailView
from books.models import Book, Page

class BookDetail(DetailView):

    def get_context_data(self, *args, **kw):
        data = super(BookDetail, self).get_context_data(*args, **kw)
        category = self.object.category
        data.update({
            'books_in_category': category.book_set.exclude(pk=self.object.id)[:4],
            'category': category
            });
        return data
    
    def get_queryset(self):
        return Book.objects.all()

class BookTOC(DetailView):
    context_object_name = 'book'
    template_name = 'books/book_toc.html'

    def get_context_data(self, *args, **kw):
        data = super(BookTOC, self).get_context_data(*args, **kw)
        return data
    
    def get_queryset(self):
        return Book.objects.all()

class ReadPage(DetailView):
    context_object_name = 'page'
    template_name = 'books/read_page.html'
    model = Page
        
