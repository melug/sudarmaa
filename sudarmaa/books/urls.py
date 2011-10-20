from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from books.views import CommonContextView

urlpatterns = patterns("",
    url(r"^$", CommonContextView.as_view(template_name="books/home.html"), name="base"),
)

