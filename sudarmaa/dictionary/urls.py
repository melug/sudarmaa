from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from dictionary.views import GetWord, ContributeWord, ThanksContribution, DiscussWord, ContributionList

urlpatterns = patterns("", 
    url(r"^word/get/$", login_required(GetWord.as_view()),
    name="get-word"),
    url(r"^word/contribute/$", login_required(ContributeWord.as_view()),
    name="contribute-word"),
    url(r"^word/discuss/(?P<pk>\d+)/$", login_required(DiscussWord.as_view()),
    name="discuss-word"),
    url(r"^word/thanks/$", login_required(ThanksContribution.as_view()),
    name="thanks-contribution"),
    url(r"^word/contributions/$", login_required(ContributionList.as_view()),
    name="contribution-list"),
    url(r"^word/discuss/$", login_required(ContributionList.as_view())),
)

