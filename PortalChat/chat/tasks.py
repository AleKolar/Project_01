from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect

from .models import CustomUser, Advertisement, Response


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


@shared_task
def send_response_notification_task(advertisement_id, response_text):
    advertisement = Advertisement.objects.get(id=advertisement_id)
    subject = 'Your Response Has Been Accepted'
    message = f'Hello {advertisement.username},\n\nYour response to the advertisement "{advertisement.title}" has been accepted.\n\nResponse: {response_text}\n\nBest regards, Your Website Team'
    send_mail(subject, message, 'your@email.com', [advertisement.username.email])


# ОТПРАВЛЯЮ УВЕДОМЛЕНИЕ
@shared_task
def send_response_email(advertisement, text):
    subject = 'ОПОВЕЩАЮ ВЫ ПОЛУЧИЛИ НОВЫЙ ОТКЛИК'
    message = f'{advertisement.username},\n\nОПОВЕЩАЮ ВЫ ПОЛУЧИЛИ НОВЫЙ ОТКЛИК"{advertisement.title}".\n\nResponse: {text}\n\nBest regards, Your Website Team'
    send_mail(subject, message, 'qefest-173@yandex.ru', [advertisement.username.email])






