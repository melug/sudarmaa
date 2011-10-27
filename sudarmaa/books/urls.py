from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from books.views import (HomeView, MyBooksView, BooksInCategory, 
    CreateBook, ShowMyBook, EditPage, EditPageContent, PagePreview)

urlpatterns = patterns("",
    url(r"^$", HomeView.as_view(template_name="books/home.html"), name="home"),
    url(r"^browse/$", BooksInCategory.as_view(
        template_name='books/books_with_category.html',
    ), name="books-in-category"),
    url(r"^my/books/$", login_required(MyBooksView.as_view()), name="my-books"),
    url(r"^my/books/create/$", login_required(CreateBook.as_view()), name="my-books-create"),
    url(r"^my/books/show/(?P<pk>\d+)/$", login_required(ShowMyBook.as_view()), name="my-books-show"),
    url(r"^my/books/preview/$", login_required(PagePreview.as_view()), name="page-preview"),
    url(r"^my/books/editpage/$", login_required(EditPage.as_view()), name="edit-page"),
    url(r"^my/books/editpage/(?P<pk>\d+)/$", login_required(EditPageContent.as_view()), name="edit-page-content"),
)

