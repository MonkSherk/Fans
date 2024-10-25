from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile, Post, Comment, Payment

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['photo', 'video', 'description', 'is_paid', 'price']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['card_number']

from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'header', 'is_private']
