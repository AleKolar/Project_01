from django import forms
from .models import CustomUser


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'username']


class AuthForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'username']


class ConfirmationForm(forms.ModelForm):
    code = forms.CharField(max_length=10)

    class Meta:
        model = CustomUser
        fields = ['code']