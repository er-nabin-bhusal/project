from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    content = forms.Textarea()
    
    class Meta:
        model = Post
        fields = [
          'title',
          'content',
          'image',
          'draft',
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "w3-input w3-border"}
            )
        }
