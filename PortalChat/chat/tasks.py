from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser



@shared_task
def send_one_time_code_email(user_id):
    user = CustomUser.objects.get(pk=user_id)
    subject = 'Your One-Time Code'
    message = f'Hello {user.username}, your one-time code is {user.code}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

@shared_task
def send_confirmation_code(user_id):
    user = CustomUser.objects.get(pk=user_id)
    send_mail('Confirmation Code', f'Your one-time code is: {user.code}', settings.EMAIL_HOST_USER, [user.email])