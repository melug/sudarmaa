from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from dictionary.views import GetWord

urlpatterns = patterns("", 
    url(r"^word/get/$", GetWord.as_view(),
    name="get-word"),
)

