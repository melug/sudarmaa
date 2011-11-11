from django.views.generic import DetailView
from books.models import Book

class BookDetail(DetailView):
    template_name = 'book_detail.html'

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
    template_name = 'book_read.html'

    def get_context_data(self, *args, **kw):
        data = super(BookDetail, self).get_context_data(*args, **kw)
        return data
    
    def get_queryset(self):
        return Book.objects.all()

        
        
