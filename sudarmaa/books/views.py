# Create your views here.
from django.views.generic import TemplateView, ListView
from books.models import Book, Category, Pick

class HomeView(TemplateView):
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data()
        context.update({
            'new_books' : Book.objects.all()[:4],
            'picked_books': Book.objects.filter(
                pick__isnull=False).order_by('pick__order_number')[:4],
            'categories' : Category.objects.all()
        })
        return context

class MyBooksView(ListView):
    context_object_name = 'my_books'

    def get_query_set(self):
        return self.request.user.book_set.all()

