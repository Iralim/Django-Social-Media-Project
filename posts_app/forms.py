from django import forms
from main.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','body','image']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter post title'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter post content'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
