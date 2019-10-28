import random

from django.conf import settings
from django.test import TestCase
from rest_framework.test import APIClient

from common.models import ABSAEvent, Review, Vendor

BASE_URL = '/v1/absa-events'
headers  = {
    'HTTP_Authorization': 'Basic ' + settings.AUTH_SERVICE['CLIENT_ID'] + ':' + settings.AUTH_SERVICE['CLIENT_SECRET'],
}

def create_absa_events(review, count=30):
    for i in range(count):
        ABSAEvent.objects.create(
            review=review,
            team_id='abc',
            term='random',
            variant='random',
            event_type=random.choice(('aspect', 'opinion',)),
            score=random.random() * random.choice((-1, 1)),
        )


class ABSAEventListViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(name='Test vendor', team_id='abc')
        self.review = Review.objects.create(
            vendor=self.vendor,
            text='This is a pretty amazing review.',
        )

    def test_no_events(self):
        """Ensures that an empty response (no data existing) looks as expected"""
        result          = self.client.get(BASE_URL, **headers)
        expected_result = {
            'count': 0,
            'next': None,
            'previous': None,
            'results': [],
        }
        self.assertDictEqual(result.data, expected_result)

    def test_with_events(self):
        create_absa_events(self.review, 30)
        result = self.client.get(BASE_URL, **headers)
        self.assertEqual(result.data['count'], 30)

    def test_filter_for_aspects(self):
        create_absa_events(self.review)
        events          = ABSAEvent.objects.all()
        aspect_count    = 0
        for e in events:
            if e.event_type == ABSAEvent.ASPECT:
                aspect_count += 1
        result = self.client.get(BASE_URL + '?event_type=aspect', **headers)
        self.assertEqual(result.data['count'], aspect_count)

    def test_filter_for_opinions(self):
        create_absa_events(self.review)
        events          = ABSAEvent.objects.all()
        opinion_count   = 0
        for e in events:
            if e.event_type == ABSAEvent.OPINION:
                opinion_count += 1
        result = self.client.get(BASE_URL + '?event_type=opinion', **headers)
        self.assertEqual(result.data['count'], opinion_count)
