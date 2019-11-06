import random

from django.conf import settings
from django.test import TestCase
from rest_framework.test import APIClient

from common.models import ABSAEvent, Review, Vendor
from ._helpers import get_client_auth_header, get_user_auth_header

BASE_URL = '/v1/absa-events'

def create_absa_events(review, count=30):
    for i in range(count):
        ABSAEvent.objects.create(
            review=review,
            team_id=settings.TESTING['team_id'],
            term='random',
            variant='random',
            event_type=random.choice(('aspect', 'opinion',)),
            score=random.random() * random.choice((-1, 1)),
        )

class ABSAEventListViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(name='Test vendor', team_id=settings.TESTING['team_id'])
        self.review = Review.objects.create(
            vendor=self.vendor,
            text='This is a pretty amazing review.',
        )

        self.client_auth_headers    = {'HTTP_Authorization':get_client_auth_header()}
        self.user_auth_headers      = {'HTTP_Authorization':get_user_auth_header()}

    def test_no_events(self):
        """Ensures that an empty response (no data existing) looks as expected"""
        expected_result = {
            'count': 0,
            'next': None,
            'previous': None,
            'results': [],
        }

        # client auth
        client_result = self.client.get(BASE_URL, **self.client_auth_headers)
        self.assertDictEqual(client_result.data, expected_result)

        # user auth
        user_result = self.client.get(BASE_URL, **self.user_auth_headers)
        self.assertDictEqual(user_result.data, expected_result)

    def test_with_events(self):
        create_absa_events(self.review, 30)

        # client auth
        client_result = self.client.get(BASE_URL, **self.client_auth_headers)
        self.assertEqual(client_result.data['count'], 30)

        # user auth
        user_result = self.client.get(BASE_URL, **self.user_auth_headers)
        self.assertEqual(user_result.data['count'], 30)

    def test_filter_for_aspects(self):
        create_absa_events(self.review)
        events          = ABSAEvent.objects.all()
        aspect_count    = 0
        for e in events:
            if e.event_type == ABSAEvent.ASPECT:
                aspect_count += 1

        # client auth
        client_result = self.client.get(BASE_URL + '?event_type=aspect', **self.client_auth_headers)
        self.assertEqual(client_result.data['count'], aspect_count)

        # user auth
        user_result = self.client.get(BASE_URL + '?event_type=aspect', **self.user_auth_headers)
        self.assertEqual(user_result.data['count'], aspect_count)

    def test_filter_for_opinions(self):
        create_absa_events(self.review)
        events          = ABSAEvent.objects.all()
        opinion_count   = 0
        for e in events:
            if e.event_type == ABSAEvent.OPINION:
                opinion_count += 1

        # client auth
        client_request = self.client.get(BASE_URL + '?event_type=opinion', **self.client_auth_headers)
        self.assertEqual(client_request.data['count'], opinion_count)

        # user auth
        user_request = self.client.get(BASE_URL + '?event_type=opinion', **self.user_auth_headers)
        self.assertEqual(user_request.data['count'], opinion_count)
