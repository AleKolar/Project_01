from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    code = forms.CharField(max_length=6, required=False)
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'code']




class AuthForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password', 'username']


class ConfirmationForm(forms.ModelForm):
    code = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = ['code']
