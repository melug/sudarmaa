from django import forms
from books.models import Book, Page, Shelf

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ('creator',)

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('title', 'content',)
        widgets = {
            'content': forms.Textarea(attrs={'rows': 25, 'class':'span14'}),
            'title': forms.TextInput(attrs={'class': 'span6'})
        }

class ShelfForm(forms.ModelForm):
    class Meta:
        model = Shelf
        exclude = ('is_public', 'books')

