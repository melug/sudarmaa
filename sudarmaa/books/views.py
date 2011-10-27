# Create your views here.
import json

from django.db.models import Max
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.views.generic import TemplateView, ListView, CreateView, DetailView, View, UpdateView
from django.shortcuts import get_object_or_404

from books.models import Book, Category, Pick, Page
from books.forms import BookForm, PageForm

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
        if action=='addpage':
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
        elif action=='deletepage':
            page_id = request.POST.get('page_id', None)
            page = get_object_or_404(Page, pk=page_id, book__creator=self.request.user)
            page.subpages.all().delete()
            page.delete()
            return HttpResponse(json.dumps(page_id))
        elif action=='swappages':
            page1_id, page2_id = request.POST.get('page1_id', None), request.POST.get('page2_id', None)
            page1 = get_object_or_404(Page, pk=page1_id, book__creator=self.request.user)
            page2 = get_object_or_404(Page, pk=page2_id, book__creator=self.request.user)
            page1.siblings_order, page2.siblings_order = page2.siblings_order, page1.siblings_order
            page1.save()
            page2.save()
            return HttpResponse(json.dumps({'page1_id': page1.id, 'page2_id': page2.id}))

class EditPageContent(UpdateView):
    form_class = PageForm

    def get_queryset(self):
        return Page.objects.filter(book__creator=self.request.user)

    def form_valid(self, form):
        f = super(EditPageContent, self).form_valid(form)
        messages.info(self.request, 'Page updated')
        return f

    def get_success_url(self):
        page = self.object
        return reverse('edit-page-content', kwargs={'pk':page.id})

class PagePreview(TemplateView):
    context_object_name = 'page'
    template_name = 'books/page_view.html'

    def get_context_data(self, **kwargs):
        context = super(PagePreview, self).get_context_data(**kwargs)
        data = self.request.POST.get('page', '')
        for t, r in (('>', '&gt;'),('<', '&lt;')):
            data = data.replace(t, r)
        context.update({'content': data})
        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

