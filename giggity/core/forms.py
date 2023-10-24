from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Post, UserProfile

class postform(ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'description', 'images', 'amount']

class userSignup(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'phone_number', 'profile_image', 'username', 'password1', 'password2']