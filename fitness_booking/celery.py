import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_booking.settings')

app = Celery('fitness_booking')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Important for timezone support
app.conf.enable_utc = True
app.conf.timezone = 'Asia/Kolkata'