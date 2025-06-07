from django.contrib import admin
from .models import FitnessClass, Booking
import pytz

# Set IST timezone
IST = pytz.timezone("Asia/Kolkata")

@admin.register(FitnessClass)
class FitnessClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'instructor', 'datetime', 'available_slots')
    list_filter = ('name', 'instructor')
    search_fields = ('name', 'instructor')
    ordering = ('datetime',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_email', 'fitness_class', 'get_booking_time_ist', 'reminder_sent')
    list_filter = ('reminder_sent', 'fitness_class__name')
    search_fields = ('client_name', 'client_email')
    ordering = ('-booking_time',)

    def get_booking_time_ist(self, obj):
        if obj.booking_time:
            ist_time = obj.booking_time.astimezone(IST)
            return ist_time.strftime('%B %d, %Y, %I:%M %p')
        return "-"
    get_booking_time_ist.short_description = 'Booking Time (IST)'
    get_booking_time_ist.admin_order_field = 'booking_time'
