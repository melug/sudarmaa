# Create your views here.
from django.views.generic import TemplateView
from books.models import Book, Category, Pick

class CommonContextView(TemplateView):
    
    def get_context_data(self, **kwargs):
        context = super(CommonContextView, self).get_context_data()
        context['book_list'] = Book.objects.all()
        return context

