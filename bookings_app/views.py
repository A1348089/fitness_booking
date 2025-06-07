from rest_framework import generics, status
from rest_framework.response import Response
from django.utils import timezone
from pytz import timezone as pytz_timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer
import logging

logger = logging.getLogger(__name__)

DEFAULT_TIMEZONE = 'Asia/Kolkata'


def convert_datetime_to_user_timezone(dt, tz_str):
    try:
        user_tz = pytz_timezone(tz_str)
    except Exception:
        user_tz = pytz_timezone(DEFAULT_TIMEZONE)

    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt)
    return dt.astimezone(user_tz)


def send_confirmation_email(email, client_name, class_name, class_datetime, user_tz_str):
    user_tz = pytz_timezone(user_tz_str)
    class_time_local = class_datetime.astimezone(user_tz)
    formatted_time = class_time_local.strftime('%Y-%m-%d %I:%M %p %Z')

    subject = f"\u2705 Booking Confirmed for {class_name}"
    message = (
        f"Hi {client_name},\n\nYour booking for '{class_name}' on {formatted_time} is confirmed.\n"
        f"Thanks for choosing us!\n\n- Fitness Team"
    )

    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
        logger.info(f"Confirmation email sent to {email}")
    except Exception as e:
        logger.error(f"Email sending failed to {email}: {str(e)}")


class FitnessClassListView(generics.ListAPIView):
    serializer_class = FitnessClassSerializer

    def get_queryset(self):
        return FitnessClass.objects.all().order_by('datetime')

    def list(self, request, *args, **kwargs):
        tz_str = request.query_params.get('tz', DEFAULT_TIMEZONE)
        classes = self.get_queryset()
        data = []

        for cls in classes:
            local_time = convert_datetime_to_user_timezone(cls.datetime, tz_str)
            data.append({
                'id': cls.id,
                'name': cls.name,
                'instructor': cls.instructor,
                'available_slots': cls.available_slots,
                'datetime': local_time.strftime('%Y-%m-%d %I:%M %p %Z')
            })

        return Response(data)


class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        tz_str = request.data.get('tz', DEFAULT_TIMEZONE)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()

        # Send confirmation email
        send_confirmation_email(
            email=booking.client_email,
            client_name=booking.client_name,
            class_name=booking.fitness_class.name,
            class_datetime=booking.fitness_class.datetime,
            user_tz_str=tz_str
        )

        return Response({"message": "Booking confirmed and email sent."}, status=status.HTTP_201_CREATED)


class BookingListByEmailView(generics.ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        email = self.request.query_params.get('email')
        return Booking.objects.filter(client_email=email) if email else Booking.objects.none()

    def list(self, request, *args, **kwargs):
        tz_str = request.query_params.get('tz', DEFAULT_TIMEZONE)
        bookings = self.get_queryset()
        data = []

        for booking in bookings:
            class_obj = booking.fitness_class
            local_class_time = convert_datetime_to_user_timezone(class_obj.datetime, tz_str)
            local_booking_time = convert_datetime_to_user_timezone(booking.booking_time, tz_str)

            data.append({
                'id': booking.id,
                'class_name': class_obj.name,
                'client_name': booking.client_name,
                'client_email': booking.client_email,
                'datetime': local_class_time.strftime('%Y-%m-%d %I:%M %p %Z'),
                'booking_time': local_booking_time.strftime('%Y-%m-%d %I:%M %p %Z'),
                'reminder_sent': booking.reminder_sent
            })
        return Response(data)
