from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import requests

from common.models import Transaction

class Command(BaseCommand):
    help = "Sends the first review request for all transactions that haven't sent a review request"

    def handle(self, *args, **options):
        transactions = Transaction.objects.filter(review_requests_sent=0).exclude(customer_email__exact='').exclude(customer_email__isnull=True)
        if len(transactions) is 0:
            self.stdout.write(self.style.NOTICE('No transactions were found with the given criteria'))
        for t in transactions:
            try:
                # send email
                response = requests.post(settings.MAILER_SERVICE['BASE_URL'], data={
                    'messageData': 'You have a new review to write!',
                    'recipientAddress': t.customer_email,
                    'originAddress': settings.MAILER_SERVICE['FROM_EMAIL'],
                    'subject': f'Leave a review for your recent order at {t.vendor.name}',
                    'scheduledSendDate': datetime.now() + timedelta(days=settings.MAILER_SERVICE['DEFAULT_DELAY_DAYS']),
                })

                # increment review_requests_sent
                t.review_requests_sent += 1
                t.save()

                self.stdout.write(self.style.SUCCESS(f'Sent review request to {t.customer_email} for transaction {t.id}'))
            except:
                self.stdout.write(self.style.ERROR('There was an error :('))
