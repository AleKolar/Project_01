# from django.test import TestCase
#
# # Create your tests here.

from django.core.mail import send_mail

send_mail(
    'Test Subject',
    'Test message body',
    'gefest-173@yandex.ru',
    ['alek.kolark@gmail.com'],
    fail_silently=False,
)

