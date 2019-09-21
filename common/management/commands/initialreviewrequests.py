from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import requests

from common.models import Transaction
from common.services.email import Email

class Command(BaseCommand):
    help = "Sends the first review request for all transactions that haven't sent a review request"

    def handle(self, *args, **options):
        transactions = Transaction.objects.filter(review_requests_sent=0).exclude(customer_email__exact='').exclude(customer_email__isnull=True)
        if len(transactions) is 0:
            self.stdout.write(self.style.NOTICE('No transactions were found with the given criteria'))
        for t in transactions:
            try:
                # send email
                email = Email(t.customer_email)
                email.send_review_request(t.vendor.name, transaction_id=t.id)

                # increment review_requests_sent
                t.review_requests_sent += 1
                t.save()

                self.stdout.write(self.style.SUCCESS(f'Sent review request to {t.customer_email} for transaction {t.id}'))
            except:
                self.stdout.write(self.style.ERROR('There was an error :('))
