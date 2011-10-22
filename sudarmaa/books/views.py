# Create your views here.
from django.views.generic import TemplateView
from books.models import Book, Category, Pick

class CommonContextView(TemplateView):
    
    def get_context_data(self, **kwargs):
        context = super(CommonContextView, self).get_context_data()
        context.update({
            'new_books' : Book.objects.all()[:4],
            'picked_books': Book.objects.filter(
                pick__isnull=False).order_by('pick__order_number')[:4],
            'categories' : Category.objects.all()
        })
        return context

