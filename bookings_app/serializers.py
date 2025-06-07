# serializers.py
from rest_framework import serializers
from .models import FitnessClass, Booking
from pytz import timezone as pytz_timezone
from datetime import timedelta
from django.utils import timezone

class FitnessClassSerializer(serializers.ModelSerializer):
    local_datetime = serializers.SerializerMethodField()

    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'instructor', 'datetime', 'available_slots', 'local_datetime']

    def get_local_datetime(self, obj):
        request = self.context.get('request')
        user_timezone_str = request.query_params.get('tz', 'Asia/Kolkata')
        try:
            user_tz = pytz_timezone(user_timezone_str)
        except Exception:
            user_tz = pytz_timezone('Asia/Kolkata')

        return obj.datetime.astimezone(user_tz).strftime('%Y-%m-%d %I:%M %p %Z')

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'fitness_class', 'client_name', 'client_email', 'booking_time', 'user_timezone']
        read_only_fields = ['booking_time']

    def validate(self, data):
        fitness_class = data.get('fitness_class')
        if fitness_class.available_slots <= 0:
            raise serializers.ValidationError("No slots available for this class.")

        current_time = timezone.now()
        if fitness_class.datetime - current_time < timedelta(minutes=10):
            raise serializers.ValidationError("Bookings must be made at least 10 minutes before the class starts.")

        if Booking.objects.filter(
            fitness_class=fitness_class,
            client_email=data['client_email']
        ).exists():
            raise serializers.ValidationError("You have already booked this class.")

        return data

    def create(self, validated_data):
        fitness_class = validated_data['fitness_class']
        fitness_class.available_slots -= 1
        fitness_class.save()
        return Booking.objects.create(**validated_data)