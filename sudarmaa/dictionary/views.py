# Create your views here.
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from django.shortcuts import redirect

from dictionary.models import Word, Suggestion
from dictionary.forms import SuggestionForm

class GetWord(TemplateView):
    template_name = 'dictionary/word_desc.html'

    def get_context_data(self, *args, **kw):
        data = super(GetWord, self).get_context_data(*args, **kw)
        word_text = self.request.REQUEST.get('w', None)
        if word_text:
            try:
                exact_word = Word.objects.get(word=word_text)
                data.update({'status': 'found','word': exact_word})
            except Word.DoesNotExist:
                suggestion_words = Word.objects.filter(word__startswith=word_text)[:5]
                if len(suggestion_words):
                    data.update({'status': 'suggestion', 'suggestions': suggestion_words})
                else:
                    data.update({'status': 'notfound', 'word_text': word_text })
        return data

class ContributeWord(CreateView):
    template_name = 'dictionary/contribute_word.html'
    form_class = SuggestionForm

    def get_initial(self):
        return { 'word': self.word }

    def get_success_url(self):
        suggestion = self.object
        suggestion.contributor = self.request.user
        suggestion.save()
        return reverse('thanks-contribution')

    def get(self, request, *args, **kw):
        self.word = self.request.REQUEST.get('s', '')
        try:
            suggestion = Suggestion.objects.get(word=self.word)
            return redirect('discuss-word', pk=suggestion.id )
        except Suggestion.DoesNotExist:
            return super(ContributeWord, self).get(request, *args, **kw)

    def post(self, request, *args, **kw):
        self.word = self.request.REQUEST.get('s', '')
        return super(ContributeWord, self).post(request, *args, **kw)

class DiscussWord(DetailView):
    template_name = 'dictionary/discuss_suggestion.html'
    model = Suggestion

class ThanksContribution(TemplateView):
    template_name = 'dictionary/thanks_contrib.html'

class ContributionList(ListView):
    context_object_name = 'suggestions'
    paginate_by = 20

    def get_queryset(self):
        return Suggestion.objects.all().order_by('-date_added')

