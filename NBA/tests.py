from django.test import TestCase
from rest_framework.test import APIClient
from .models import Schedule  # Import your Schedule model
from .searlizer import ReactSerializer  # Import your ReactSerializer


class TeamScheduleViewTestCase(TestCase):
    def setUp(self):
        # creating test objects
        Schedule.objects.create(
            team='ATL', date='2023-09-21', opponent='Opponent 1')
        Schedule.objects.create(
            team='BOS', date='2023-09-22', opponent='Opponent 2')

    def test_get_team_schedule(self):
        # an instance of the APIClient for making API requests
        client = APIClient()

        # Make a GET request to your view with a team abbreviation
        response = client.get('/nba/schedule/BOS/')

        # Assert the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
