from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from books.views import HomeView, MyBooksView, BooksInCategory

urlpatterns = patterns("",
    url(r"^$", HomeView.as_view(template_name="books/home.html"), name="home"),
    url(r"^my/books/$", login_required(MyBooksView.as_view()), name="my-books"),
    url(r"^browse/$", BooksInCategory.as_view(
        template_name='books/books_with_category.html',
    ), name="books-in-category"),
)

