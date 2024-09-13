import random
import string
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect
from .forms import AuthForm, RegistrationForm, ConfirmationForm
from django import forms
from .tasks import send_confirmation_code, send_one_time_code_email
from .models import CustomUser


def generate_confirmation_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def clean_email(self):
    email = self.cleaned_data['email']
    if CustomUser.objects.filter(email=email).exists():
        raise forms.ValidationError("Такой E-mail уже существует!")
    return email


# def login_user(request):
#     if request.method == 'POST':
#         form = AuthForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             username = form.cleaned_data['username']
#             code = generate_confirmation_code()
#             request.session['confirmation_code'] = code
#
#             user = authenticate(request, username=username, password=password)
#
#             if user is not None:
#                 send_confirmation_code.delay(user.pk)
#
#                 print(f'Confirmation code sent to user: {code}')
#
#                 return redirect('verify_code')
#
#     else:
#         form = AuthForm()
#
#     return render(request, 'login.html', {'form': form})


def confirm_code(request):
    if request.method == 'POST':
        form = ConfirmationForm(request.POST)
        if form.is_valid():
            code_entered = form.cleaned_data['code']
            user = request.user
            code_stored = user.customuser.code

            if code_entered == code_stored:

                return redirect('home')
            else:
                return redirect('registration')

    else:
        form = ConfirmationForm()

    return render(request, 'confirm_code_template.html', {'form': form})


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            code = generate_confirmation_code()
            user.code = code
            user.save()
            expiration_time = timezone.now() + timedelta(seconds=120)
            send_one_time_code_email.delay(user.pk)

            print(f'One-time code generated: {code}')

            return render(request, 'verify_code.html', {'form': form})
        else:
            return render(request, 'registration.html', {'form': form})
    else:
        form = RegistrationForm()
        return render(request, 'registration.html', {'form': form})


def verify_code_view(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        user = CustomUser.objects.get(code=code)
        user.is_verified = True
        user.save()
        return render(request, 'registration_success.html')
    return render(request, 'verify_code.html')


def home(request):
    return render(request, 'registration_success.html')


def login_user(request):
    if request.user.is_authenticated:
        user = request.user

        send_confirmation_code.delay(user.pk)
        print(f'Confirmation code sent to user: {user.code}')

        return redirect('verify_code')

    return render(request, 'login.html', {'form': AuthenticationForm()})


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    extra_context = {'title': "Авторизация"}

    def form_valid(self, form):
        response = super().form_valid(form)

        user = self.request.user
        code = generate_confirmation_code()
        user.code = code
        user.save()
        send_confirmation_code.delay(user.id)

        return response




