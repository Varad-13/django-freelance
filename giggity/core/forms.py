from django import forms
from .models import Post, Tag, Post_tag

class PostForm(forms.ModelForm):
    images = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'input'}))

    class Meta:
        model = Post
        fields = ['name', 'description', 'images', 'amount']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Name of your Service', 'required':True}),
            'description': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Describe your Service', 'required':True}),
            'amount': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Amount', 'required':True})
        }

class PostTagForm(forms.ModelForm):
    class Meta:
        model = Post_tag
        fields = ['tag']
        widgets = {
            'tag': forms.CheckboxSelectMultiple,
        }
