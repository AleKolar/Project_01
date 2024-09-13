from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    code = forms.CharField(max_length=6, required=False)
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'code']

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user


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
