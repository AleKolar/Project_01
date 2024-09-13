from django.conf import settings
from django.contrib.auth.models import User, AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    code = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    # class Meta:
    #     swappable = 'AUTH_USER_MODEL'


class Group(models.Model):
    custom_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='custom_user_groups')


class Permission(models.Model):
    custom_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='custom_user_permissions')


class Advertisement(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    category_choices = [
        ('Tanks', 'Танки'),
        ('Healers', 'Хилы'),
        ('DPS', 'ДД'),
        ('Traders', 'Торговцы'),
        ('Guild Masters', 'Гилдмастеры'),
        ('Quest Givers', 'Квестгиверы'),
        ('Blacksmiths', 'Кузнецы'),
        ('Leatherworkers', 'Кожевники'),
        ('Alchemists', 'Зельевары'),
        ('Spellcasters', 'Мастера заклинаний'),
    ]
    category = models.CharField(max_length=20, choices=category_choices)


class Response(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    text = models.TextField()


class Newsletter(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)

