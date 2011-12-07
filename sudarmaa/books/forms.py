from django import forms
from django.utils.translation import ugettext_lazy as _

from books.models import Book, Page, Shelf, Author
from gallery.models import MPhoto

class BookForm(forms.ModelForm):
    photo2 = forms.ImageField(label=_('Photo'), help_text=_('Or choose an image from below'), required=False)

    class Meta:
        model = Book
        fields = ('title', 'category', 'photo2', 'photo', 'description', 'authors', 'language')
        exclude = ('creator', 'status')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 15, 'class':'span6'}),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        photo2, photo = cleaned_data.get('photo2'), cleaned_data.get('photo')
        if not photo2 and not photo:
            raise forms.ValidationError(_('Image required'))
        if photo2:
            cleaned_data['photo'] = MPhoto.objects.create(title='', image=photo2)
        return cleaned_data

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        exclude = ('user',)
        widgets = {
            'biography': forms.Textarea(attrs={'rows': 15, 'class':'span6'}),
        }

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

