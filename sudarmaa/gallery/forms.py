from django import forms
from photologue.models import Photo

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('title', 'image')

    def clean_title_slug(self):
        data = self.cleaned_data['title']
        return data

