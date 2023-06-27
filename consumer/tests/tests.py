from django.urls import reverse
from django.test import TestCase
from django.contrib.gis.geos import Point
import csv
import tempfile
import os
from consumer.management.commands.loaddata import Command
from ..models import Consumer
from .consumer_data import sample_data
from .load_test import load_test_data


class ConsumerListAPIViewTest(TestCase):
    def setUp(self):
        # Create some sample consumer objects
        for data in sample_data:
            Consumer.objects.create(
                id=data['id'],
                street=data['street'],
                status=data['status'],
                previous_jobs_count=data['previous_jobs_count'],
                amount_due=data['amount_due'],
                location=Point(*data['location'])
            )

    def test_filter_consumers_by_min_previous_jobs_count(self):
        url = reverse('consumer-list')
        response = self.client.get(url, {'min_previous_jobs_count': 3})
        self.assertEqual(response.status_code, 200)
        self.assertIn('type', response.json()['results'])

    def test_filter_consumers_by_max_previous_jobs_count(self):
        url = reverse('consumer-list')
        response = self.client.get(url, {'max_previous_jobs_count': 3})
        self.assertEqual(response.status_code, 200)
        self.assertIn('type', response.json()['results'])

    def test_filter_consumers_by_exact_previous_jobs_count(self):
        url = reverse('consumer-list')
        response = self.client.get(url, {'previous_jobs_count': 3})
        self.assertEqual(response.status_code, 200)
        self.assertIn('type', response.json()['results'])

    def test_filter_consumers_by_status(self):
        url = reverse('consumer-list')
        response = self.client.get(url, {'status': 'active'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('type', response.json()['results'])

    def test_pagination(self):
        url = reverse('consumer-list')
        
        # Make a request to page 3
        page3_url = url + '?page=3'
        page3_response = self.client.get(page3_url)
        
        # Verify that the request to page 3 is successful
        self.assertEqual(page3_response.status_code, 200)
        
        # Extract the next and previous page URLs from the response
        next_page_url = page3_response.json()['next']
        previous_page_url = page3_response.json()['previous']
        
        # Make a request to the previous page (page 2)
        previous_page_response = self.client.get(previous_page_url)
        
        # Verify that the request to the previous page is successful
        self.assertEqual(previous_page_response.status_code, 200)
        
        # Make a request to the next page (page 3)
        next_page_response = self.client.get(next_page_url)
        
        # Verify that the request to the next page is successful
        self.assertEqual(next_page_response.status_code, 200)
        
        # Verify the number of results in the response(default page size)
        self.assertEqual(len(previous_page_response.json()['results']["features"]), 10)
        self.assertEqual(len(next_page_response.json()['results']["features"]), 10)

    def test_pagination_edge_cases(self):
        url = reverse('consumer-list')

        # Make a request to an invalid page number
        invalid_page_url = url + '?page=9999'
        invalid_page_response = self.client.get(invalid_page_url)

        # Verify that the request to an invalid page number returns a 404 status code
        self.assertEqual(invalid_page_response.status_code, 404)

        # Make a request without specifying a page number
        no_page_url = url
        no_page_response = self.client.get(no_page_url)

        # Verify that the request without a page number returns the first page
        self.assertEqual(no_page_response.status_code, 200)
        self.assertEqual(no_page_response.json()['previous'], None)
        self.assertNotEqual(no_page_response.json()['next'], None)

        # Extract the next page URL from the response
        next_page_url = no_page_response.json()['next']

        # Make a request to the next page
        next_page_response = self.client.get(next_page_url)

        # Verify that the request to the next page is successful
        self.assertEqual(next_page_response.status_code, 200)

        # Verify the number of results in the response (default page size)
        self.assertEqual(len(next_page_response.json()['results']['features']), 10)


    def test_loading_data_to_db(self):
            # Create a temporary CSV file
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as csv_file:
                # Write the sample data to the CSV file
                writer = csv.DictWriter(csv_file, fieldnames=['id', 'street', 'status', 'previous_jobs_count', 'amount_due', 'lat', 'lng'])
                writer.writeheader()
                for data in load_test_data:
                    writer.writerow({
                        'id': data['id'],
                        'street': data['street'],
                        'status': data['status'],
                        'previous_jobs_count': data['previous_jobs_count'],
                        'amount_due': data['amount_due'],
                        'lat': data['location'][1],
                        'lng': data['location'][0],
                    })

                # Close the CSV file
                csv_file.close()

                # Call the loaddata command with the temporary CSV file
                command = Command()
                command.handle(csv_file=csv_file.name)

            # Verify that the data is loaded correctly
            last_entry = Consumer.objects.last()
            last_data = load_test_data[-1]
            self.assertEqual(last_entry.id, last_data['id'])
            self.assertEqual(last_entry.street, last_data['street'])
            self.assertEqual(last_entry.status, last_data['status'])
            self.assertEqual(last_entry.previous_jobs_count, last_data['previous_jobs_count'])
            self.assertEqual(last_entry.amount_due, last_data['amount_due'])
            self.assertAlmostEqual(last_entry.location.x, last_data['location'][0], places=6)
            self.assertAlmostEqual(last_entry.location.y, last_data['location'][1], places=6)

            # Delete the temporary CSV file
            os.remove(csv_file.name)

    def test_consumer_detail_view(self):
        consumer = Consumer.objects.last()
        url = reverse('consumer-detail', kwargs={'pk': consumer.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_properties = response.json()['properties']

        # Verify that the returned consumer matches the expected data
        self.assertEqual(response_properties['id'], consumer.id)
        self.assertEqual(response_properties['street'], consumer.street)
        self.assertEqual(response_properties['status'], consumer.status)
        self.assertEqual(response_properties['previous_jobs_count'], consumer.previous_jobs_count)
        self.assertEqual(response_properties['amount_due'], consumer.amount_due)