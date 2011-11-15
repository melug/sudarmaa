from django import forms
from dictionary.models import Word, Suggestion

class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        exclude = ('contributor',)

