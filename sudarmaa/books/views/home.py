# Create your views here.
from django.views.generic import TemplateView, ListView, DetailView, View
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from books.models import Book, Category, Shelf

class HomeView(TemplateView):
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({
            'new_books' : Book.objects.all()[:4],
            'picked_books': Book.objects.filter(
                pick__isnull=False).order_by('pick__order_number')[:4],
            'categories' : Category.objects.all()
        })
        return context

class MyBooksView(ListView):
    context_object_name = 'my_books'
    paginate_by = 10

    def get_queryset(self):
        return self.request.user.book_set.all()

class BooksInCategory(ListView):
    context_object_name = 'books'
    paginate_by = 3

    def get_queryset(self):
        category_id = self.request.GET.get('cat', None)
        if category_id:
            query_set = Book.objects.filter(category__id=category_id)
        else:
            query_set = Book.objects.all()
        return query_set

    def get_context_data(self, **kwargs):
        context = super(BooksInCategory, self).get_context_data(**kwargs)
        context.update({
            'categories' : Category.objects.all()
        })
        category_id = self.request.GET.get('cat', None)
        if category_id: context.update({ 'cat' : category_id })
        return context

class ShelfView(DetailView):
    template_name = 'books/shelf_detail.html'
    context_object_name = 'shelf'
    
    def get_queryset(self):
        return Shelf.objects.filter(is_public=True)

    def get_context_data(self, *args, **kw):
        data = super(ShelfView, self).get_context_data(*args, **kw)
        data.update({
            'books' : self.object.books
        })
        return data

class ShelfList(View):

    def dispatch(self, request, *args, **kw):
        default_shelf = request.user.shelves.get(title='read')
        return redirect(reverse('shelf-detail', kwargs={ 'pk' : default_shelf.id }))

