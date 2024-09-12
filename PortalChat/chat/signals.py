import code

from django.contrib.auth import user_logged_in
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import CustomUser



@receiver(post_save, sender=CustomUser)
def send_one_time_code_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Your One-Time Code'
        message = f'Hello {instance.user.username}, your one-time code is {instance.code}'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [instance.email])


@receiver(user_logged_in)
def send_confirmation_code(sender, user, request, **kwargs):
    send_mail(
        'Confirmation Code',
        f'Your one-time code is: {user.code}',
        settings.EMAIL_HOST_USER,
        [user.customuser.email],
        fail_silently=False
    )
