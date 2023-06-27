import csv
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from consumer.models import Consumer

class Command(BaseCommand):
    help = 'Load data from csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        consumers = []

        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                location = Point(float(row['lng']), float(row['lat']))
                consumer = Consumer(
                    id=int(row['id']),
                    street=row['street'],
                    status=row['status'],
                    previous_jobs_count=int(row['previous_jobs_count']),
                    amount_due=int(row['amount_due']),
                    location=location
                )
                consumers.append(consumer)

            Consumer.objects.bulk_create(consumers)

        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))