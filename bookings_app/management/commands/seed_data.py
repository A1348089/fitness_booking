from django.core.management.base import BaseCommand
from bookings_app.models import FitnessClass
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Seed the database with sample fitness classes'

    def handle(self, *args, **kwargs):
        FitnessClass.objects.all().delete()
        now = timezone.now()

        data = [
            {'name': 'Yoga', 'instructor': 'Naidu', 'datetime': now + timedelta(minutes=15), 'available_slots': 10},
            {'name': 'Zumba', 'instructor': 'Ramesh', 'datetime': now + timedelta(minutes=20), 'available_slots': 5},
            {'name': 'HIIT', 'instructor': 'Ramesh', 'datetime': now + timedelta(minutes=30), 'available_slots': 3},
        ]

        for item in data:
            FitnessClass.objects.create(**item)

        self.stdout.write(self.style.SUCCESS('Sample fitness classes created successfully.'))