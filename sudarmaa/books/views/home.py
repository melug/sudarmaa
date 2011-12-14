# Create your views here.
import json

from django.views.generic import TemplateView, ListView, DetailView, View, CreateView
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from books.models import Book, Category, Author, AccessHistory

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
    paginate_by = None

    def get_queryset(self):
        return self.request.user.book_set.order_by('status', 'added')

class BooksInCategory(ListView):
    context_object_name = 'books'
    paginate_by = 4

    def get_queryset(self):
        category_id = self.request.GET.get('cat', None)
        latest = self.request.GET.get('latest', None)
        staff_pick = self.request.GET.get('staff_pick', None)
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

class StaffPicks(BooksInCategory):
    paginate_by = None
    
    def get_queryset(self):
        return super(StaffPicks, self).get_queryset().filter(pick__isnull=False)

class LatestBooks(BooksInCategory):
    paginate_by = None
    books_size = 10

    def get_queryset(self):
        return super(LatestBooks, self).get_queryset().order_by('-added')[:self.books_size]

class AuthorView(DetailView):
    model = Author
    template_name = 'books/author_detail.html'
    template_object_name = 'author'

class AccessHistoryList(ListView):

    def get_queryset(self):
        return AccessHistory.objects.filter(user=self.request.user).order_by('-last_access')

