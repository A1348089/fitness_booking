# tasks.py (adjusted for user timezone)
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Booking
from pytz import timezone as pytz_timezone
import logging

logger = logging.getLogger(__name__)
IST = pytz_timezone('Asia/Kolkata')

@shared_task(bind=True)
def send_reminder_emails(self):
    now = timezone.now()
    reminder_time = now + timezone.timedelta(minutes=5)
    bookings = Booking.objects.filter(
        reminder_sent=False,
        fitness_class__datetime__range=(now, reminder_time)
    )
    for booking in bookings:
        try:
            class_time = booking.fitness_class.datetime
            if timezone.is_naive(class_time):
                class_time = timezone.make_aware(class_time)

            user_tz_str = booking.user_timezone or 'Asia/Kolkata'
            user_tz = pytz_timezone(user_tz_str)
            class_time_local = class_time.astimezone(user_tz)
            formatted_time = class_time_local.strftime('%Y-%m-%d %I:%M %p %Z')

            subject = f"\U0001F551 Reminder: {booking.fitness_class.name} starts soon!"
            message = (
                f"Hi {booking.client_name},\n\n"
                f"Your class '{booking.fitness_class.name}' is scheduled at {formatted_time}.\n"
                f"Don't be late!\n\n- Fitness Team"
            )
            send_mail(subject, message, 'paravind8811@gmail.com', [booking.client_email])
            booking.reminder_sent = True
            booking.save()
        except Exception as e:
            logger.error(f"Failed to send reminder to {booking.client_email}: {str(e)}")
