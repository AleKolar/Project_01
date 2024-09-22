from rest_framework import serializers
from .models import Newsletter, CustomUser


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ['title', 'content']



