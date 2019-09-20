from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
import requests

from common.models import Review

class Command(BaseCommand):
    help = "Gets sentiment analysis for all reviews without the sentiment_analysis field set"

    def handle(self, *args, **options):
        reviews = Review.objects.filter(
            Q(sentiment_analysis__isnull=True)
            | Q(analytics_id__isnull=True)
        )
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

            self.stdout.write(self.style.SUCCESS(f'Analyzed review for {r.vendor} with id {r.id}'))
