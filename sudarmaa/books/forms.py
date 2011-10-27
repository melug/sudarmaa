from django import forms
from books.models import Book, Page

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ('creator',)

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('title', 'content',)
        widgets = {
            'content': forms.Textarea(attrs={'cols': 120, 'rows': 40, 'class':'span12'}),
            'title': forms.TextInput(attrs={'class': 'span6'})
        }

