from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))
    class Meta():
        model = User
        fields=[
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2'
        ]
class ProfileForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields = [
            'photo_profile',
            'type_profile'
        ]