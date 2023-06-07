from django import forms
from .models import *


class Blog_form(forms.ModelForm):
    class Meta:
        model = Users_blog
        fields = ('blog', 'content')
        widgets = {
            'blog': forms.Textarea()
        }