# Create your views here.
import json

from django.db.models import Max
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, CreateView, DetailView, View
from django.shortcuts import get_object_or_404

from books.models import Book, Category, Pick, Page
from books.forms import BookForm

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

class CreateBook(CreateView):
    template_name = 'books/book_form.html'
    form_class = BookForm

    def get_success_url(self):
        book = self.object
        book.creator = self.request.user
        book.save()
        return reverse('my-books-show', kwargs={'pk':book.id})

class ShowMyBook(DetailView):
    context_object_name = 'book'
    template_name = 'books/my_book.html'

    def get_queryset(self):
        return Book.objects.filter(creator=self.request.user)

class EditPage(View):
    
    def post(self, request):
        action = request.POST.get('action', None)
        if action == 'addpage':
            parent_id, book_id, title = request.POST.get('parent_page', None), request.POST.get('book_id'), request.POST.get('title')
            book = get_object_or_404(Book, creator=self.request.user, pk=book_id)
            if parent_id:
                parent_page = get_object_or_404(Page, book=book, pk=parent_id)
                max_order = parent_page.subpages.aggregate(Max('siblings_order'))['siblings_order__max'] or 0
                response_context = { 'parent_id': parent_id }
            else:
                parent_page = None
                max_order = book.page_set.aggregate(Max('siblings_order'))['siblings_order__max'] or 0
                response_context = { 'parent_id': None }
            page = Page.objects.create(parent_page=parent_page, book=book, title=title, siblings_order=max_order+1)
            response_context.update({'page_id': page.id, 'title': page.title })
            return HttpResponse(json.dumps(response_context))
        
