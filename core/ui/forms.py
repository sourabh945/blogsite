from django import forms 
from django.db import models

class blogCreateForm(forms.Form):

    title = forms.CharField(
        max_length=126,
        required=True,
        widget=forms.TextInput(attrs={'placeholder':'Enter your blog title'})
    )

    content = forms.CharField(
        max_length=126,
        required=True,
        widget=forms.Textarea(attrs={'placeholder':'Enter your blog here ...'})
    )