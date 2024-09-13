import random
import string
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect
from .forms import AuthForm, RegistrationForm, ConfirmationForm
from .models import CustomUser
from .tasks import send_confirmation_code, send_one_time_code_email


def generate_confirmation_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def login_user(request):
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            code = generate_confirmation_code()
            user = authenticate(request, user=request.user, code=code)

            if user is not None:
                send_confirmation_code.delay(user.pk)

                print(f'Confirmation code sent to user: {code}')

                return redirect('verify_code')

    else:
        form = AuthForm()

    return render(request, 'login.html', {'form': form})


def confirm_code(request):
    if request.method == 'POST':
        form = ConfirmationForm(request.POST)
        if form.is_valid():
            code_entered = form.cleaned_data['code']
            user = request.user  # Assuming user is authenticated
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
            code = generate_confirmation_code()
            user = form.save(commit=False)
            user.code = code
            user.save()
            expiration_time = timezone.now() + timedelta(seconds=60)
            send_one_time_code_email.delay(user.pk)

            print(f'One-time code generated: {code}')

            return render(request, 'verify_code.htm', {'form': form})
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
