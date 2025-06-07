# models.py
from django.db import models

class FitnessClass(models.Model):
    CLASS_CHOICES = [
    ('Yoga', 'Yoga'),
    ('Zumba', 'Zumba'),
    ('HIIT', 'HIIT'),]
    name = models.CharField(max_length=100, choices=CLASS_CHOICES)
    instructor = models.CharField(max_length=100)
    datetime = models.DateTimeField()  # Stored in IST
    available_slots = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} with {self.instructor} on {self.datetime}"

class Booking(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    booking_time = models.DateTimeField(auto_now_add=True)
    reminder_sent = models.BooleanField(default=False)
    user_timezone = models.CharField(max_length=64, default='Asia/Kolkata')  # New

    def __str__(self):
        return f"{self.client_name} - {self.fitness_class}"