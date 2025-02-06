
from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

import environ

env = environ.Env()
environ.Env.read_env()

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=100, required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    

class CustomerLoginForm(forms.Form):
    email = forms.EmailField(
        label='email',
        max_length=100,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        label='password',
        max_length=100,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )