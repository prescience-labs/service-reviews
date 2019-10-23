import time

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
import requests

from common.models import ABSAEvent, Review

class Command(BaseCommand):
    help = "Gets sentiment analysis for all reviews without the sentiment_analysis field set"

    def handle(self, *args, **options):
        reviews = Review.objects.filter(
            Q(sentiment_analysis__isnull=True)
            | Q(analytics_id__isnull=True)
        )[:2000]
        if len(reviews) is 0:
            self.stdout.write(self.style.NOTICE('No reviews were found with the given criteria'))
        for r in reviews:
            response = requests.post(settings.DOCUMENTS_SERVICE['BASE_URL'] + '/documents', data={
                'text': r.text,
            })
            data                    = response.json()
            r.sentiment_analysis    = data['sentiment_analysis']
            r.analytics_id          = data['id']
            r.save()

            for event in data['sentiment_analysis']['events']:
                ABSAEvent.objects.create(
                    term=event.get('term', None),
                    variant=event.get('variant', None),
                    score=event.get('polarity', 0),
                    event_type=ABSAEvent.OPINION if event.get('type', None) == 'opinion' else ABSAEvent.ASPECT,
                    start=event.get('start', None),
                    end=event.get('end', None),
                    review=r,
                    team_id=r.vendor.team_id,
                )

            self.stdout.write(self.style.SUCCESS(f'Analyzed review for {r.vendor} with id {r.id}'))
            self.stdout.write(self.style.NOTICE('Sleeping for 0.5 seconds'))
            time.sleep(0.5)
