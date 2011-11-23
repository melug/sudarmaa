# Create your views here.
import json

from django.views.generic import TemplateView, ListView, DetailView, View, CreateView
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from books.models import Book, Category, Shelf
from books.forms import ShelfForm

class HomeView(TemplateView):
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({
            'new_books' : Book.publish.all()[:4],
            'picked_books': Book.publish.filter(
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
    paginate_by = 8

    def get_queryset(self):
        category_id = self.request.GET.get('cat', None)
        if category_id:
            query_set = Book.publish.filter(category__id=category_id)
        else:
            query_set = Book.publish.all()
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
            'books' : self.object.books,
            'shelf_form': ShelfForm()
        })
        return data

class ShelfList(View):

    def dispatch(self, request, *args, **kw):
        default_shelf = request.user.shelves.get(title='read')
        return redirect(reverse('shelf-detail', kwargs={ 'pk' : default_shelf.id }))

class ShelfCreate(View):

    def post(self, request, *args, **kw):
        title = request.POST['title']
        try:
            shelf = Shelf.objects.create(title=title, user=self.request.user)
            return HttpResponse('OK')
        except:
            return HttpResponse('Fail')

class AddBookToShelf(View):

    def post(self, request, *args, **kw):
        try:
            book_id = int(request.REQUEST.get('b', 0))
            book = Book.objects.get(status=2, pk=book_id)
            shelf_id = int(request.REQUEST.get('s', 0))
            shelf = Shelf.objects.get(user=request.user, pk=shelf_id)
            if shelf.books.filter(pk=book.id).count() == 0:
                shelf.books.add(book)
                return HttpResponse(json.dumps({'status': 'ok'}))
            else:
                return HttpResponse(json.dumps({'status': 'duplicated'}))
        except (ValueError, Book.DoesNotExist):
            return HttpResponse(json.dumps({'error': 9}))

