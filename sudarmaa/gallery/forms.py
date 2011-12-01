from django import forms
from gallery.models import MPhoto

class PhotoForm(forms.ModelForm):
    class Meta:
        model = MPhoto
        fields = ('title', 'image')

