from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect

from .models import CustomUser, Advertisement, Response, Newsletter


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
def send_accept_response_task(response_id, text):
    response = Response.objects.get(id=response_id)
    advertisement = response.advertisement
    user_id = response.user_id

    user = CustomUser.objects.get(id=user_id)

    subject = 'Ваш Отклик принят'
    message = f'Hello {user.username},\n\nYour response to the advertisement "{advertisement.title}" has been accepted.\n\nResponse: {text}\n\nBest regards, Your Website Team'

    send_mail(subject, message, 'gefest-173@yandex.ru', [user.email])


# ОТПРАВЛЯЮ УВЕДОМЛЕНИЕ
@shared_task
def send_response_email(advertisement_id, text):
    advertisement = Advertisement.objects.get(id=advertisement_id)

    subject = 'ОПОВЕЩАЮ ВЫ ПОЛУЧИЛИ НОВЫЙ ОТКЛИК'
    message = f'{advertisement.user.username},\n\nОПОВЕЩАЮ ВЫ ПОЛУЧИЛИ НОВЫЙ ОТКЛИК "{advertisement.title}".\n\nResponse: {text}\n\nBest regards, Your Website Team'
    send_mail(subject, message, 'qefest-173@yandex.ru', [advertisement.user.email])


@shared_task
def send_newsletter_task(newsletter_id):
    newsletter = Newsletter.objects.get(pk=newsletter_id)
    recipients = newsletter.recipients.all()
    subject = newsletter.title
    message = newsletter.content
    recipient_emails = recipients.values_list('email', flat=True)

    send_mail(subject, message, 'admin@example.com', recipient_emails)


