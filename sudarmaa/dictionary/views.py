# Create your views here.
from django.http import HttpResponse
from django.views.generic import TemplateView

from dictionary.models import Word

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
                    data.update({'status': 'notfound'})
        return data

