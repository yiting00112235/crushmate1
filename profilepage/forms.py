from django import forms
from .models import ProfilePhoto

class PhotoForm(forms.ModelForm):
    class Meta:
        model = ProfilePhoto
        fields = ['image']