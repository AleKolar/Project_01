from celery import Celery

app = Celery('chat', broker='amqp://guest:guest@localhost//')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()