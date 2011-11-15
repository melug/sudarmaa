from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from dictionary.views import GetWord, ContributeWord, ThanksContribution, DiscussWord

urlpatterns = patterns("", 
    url(r"^word/get/$", GetWord.as_view(),
    name="get-word"),
    url(r"^word/contribute/$", ContributeWord.as_view(),
    name="contribute-word"),
    url(r"^word/discuss/(?P<pk>\d+)/$", DiscussWord.as_view(),
    name="discuss-word"),
    url(r"^word/thanks/$", ThanksContribution.as_view(),
    name="thanks-contribution"),
)

