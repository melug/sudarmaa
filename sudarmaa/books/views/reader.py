import json

from django.views.generic import DetailView, View, ListView
from django.http import HttpResponse
from djangoratings.views import AddRatingFromModel

from books.models import Book, Page, Bookmark

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
        return Book.publish.all()

class BookTOC(DetailView):
    context_object_name = 'book'
    template_name = 'books/book_toc.html'

    def get_context_data(self, *args, **kw):
        data = super(BookTOC, self).get_context_data(*args, **kw)
        return data
    
    def get_queryset(self):
        return Book.publish.all()

class ReadPage(DetailView):
    context_object_name = 'page'
    template_name = 'books/read_page.html'
    model = Page

    def get_context_data(self, *args, **kw):
        data = super(ReadPage, self).get_context_data(*args, **kw)
        data.update({
            'book': self.object.book
        })
        return data
        
class AddRating(View):
    
    def post(self, request, *args, **kwargs):
        params = {
            'app_label': 'books',
            'model': 'book',
            'field_name': 'rating'
        }
        params.update(kwargs)
        response = AddRatingFromModel()(request, **params)
        if response.status_code == 200:
            return HttpResponse(json.dumps({'message': response.content}))
        return HttpResponse(json.dumps({'error': 9, 'message': response.content}))

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class BookmarkAdd(View):

    def post(self, request, *args, **kwargs):
        try:
            page_id = int(kwargs['page_id'])
            page = Page.objects.get(pk=page_id)
            book = page.book
            if book.status == 2:
                bookmarks = Bookmark.objects.filter(user=request.user, page=page)
                if bookmarks.count() == 0:
                    bookmark = Bookmark.objects.create(user=request.user, page=page)
                    return HttpResponse(json.dumps({'status': 'ok'}))
                else:
                    return HttpResponse(json.dumps({'error': 'already created'}))
            else:
                return HttpResponse(json.dumps({'error': 9}))
        except Exception, e:
            return HttpResponse(json.dumps({'error': 10}))

class BookmarkRemove(View):

    def post(self, request, *args, **kwargs):
        try:
            page_id = int(kwargs['page_id'])
            page = Page.objects.get(pk=page_id)
            bookmark = Bookmark.objects.get(user=request.user, page=page)
            bookmark.delete()
            return HttpResponse(json.dumps({'status': 'deleted'}))
        except:
            return HttpResponse(json.dumps({'error': 10}))

class BookmarksView(ListView):
    
    def get_queryset(self, *args, **kw):
        return Bookmark.objects.filter(user=self.request.user)

