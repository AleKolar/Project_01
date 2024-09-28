from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import Advertisement

content_type = ContentType.objects.get_for_model(Advertisement)

custom_permissions = [
    Permission.objects.create(codename='custom_add_advertisement', name='Can add custom advertisement', content_type=content_type),
    Permission.objects.create(codename='custom_change_advertisement', name='Can change custom advertisement', content_type=content_type),
]