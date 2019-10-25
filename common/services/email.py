from datetime import datetime, timedelta
import logging

from django.conf import settings
from django.template.loader import render_to_string
import requests

logger = logging.getLogger(__name__)

class Email:
    def __init__(self, recipient, subject=None, content=None):
        """Create a new Email

        Args:
        - recipient (string): Should be of the type "email@example.com" or possibly "First Last <email@example.com>"
        - subject (string, optional): The subject of the email. Defaults to None.
        - content (string, optional): The content of the email. It will be sent as an HTML email, so sending HTML here is expected. Defaults to None.
        """
        self.recipient  = recipient
        self.subject    = subject
        self.content    = content

    def send_review_request(self, vendor_name, product_name=None, transaction_id=None):
        """Send an opinionated review request email

        Args:
        - product_name (string): The name of the product for the review request.
        """
        try:
            email_delay_days    = settings.MAILER_SERVICE['DEFAULT_DELAY_DAYS']
            self.subject        = f'Tell us about your order from {vendor_name}'
            self.content        = render_to_string('common/email_review_request.html', context={
                'vendor_name': vendor_name,
                'review_request_link': f'https://app.dataintel.ai/review/{transaction_id}' if transaction_id else 'https://app.dataintel.ai',
            })

            post_url    = f'{settings.MAILER_SERVICE["BASE_URL"]}/mailer/schedule'
            logger.debug(f'POST {post_url}')
            post_data   = {
                'messageData':          self.content,
                'recipientAddress':     self.recipient,
                'originAddress':        'postmaster@mg.altamir.io',
                'subject':              self.subject,
                'scheduledSendDate':    (datetime.utcnow() + timedelta(days=email_delay_days)).isoformat(),
            }
            logger.debug(post_data)

            return requests.post(post_url, post_data)
        except:
            raise Exception("Unable to request to the mailer service")
