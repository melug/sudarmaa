from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from books.views import HomeView, MyBooksView

print 'bla bla'
urlpatterns = patterns("",
    url(r"^my/books/$", login_required(MyBooksView.as_view()), name="my-books"),
    url(r"^$", HomeView.as_view(template_name="books/home.html"), name="home"),
)

