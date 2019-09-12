from datetime import datetime, timedelta
import logging

from django.conf import settings
import requests

logger = logging.getLogger(__name__)

class Email:
    def __init__(self, recipient, subject=None, content=None):
        """Create a new Email

        Args:
            recipient (string): Should be of the type "email@example.com" or possibly "First Last <email@example.com>"
            subject (string, optional): The subject of the email. Defaults to None.
            content (string, optional): The content of the email. It will be sent as an HTML email, so sending HTML here is expected. Defaults to None.
        """
        self.recipient  = recipient
        self.subject    = subject
        self.content    = content

    def send_review_request(self, product_name):
        """Send an opinionated review request email

        Args:
            product_name (string): The name of the product for the review request.
        """
        email_delay_days    = 7
        self.subject        = f'Tell us about your order of {product_name}'
        self.content        = f"Thanks for purchasing {product_name}! Let us know what you thought: CLICK HERE"

        post_url    = f'{settings.MAILER_SERVICE["BASE_URL"]}/mailer/schedule'
        post_data   = {
            'messageData':          self.content,
            'recipientAddress':     self.recipient,
            'originAddress':        'postmaster@mg.altamir.io',
            'subject':              self.subject,
            'scheduledSendDate':    (datetime.utcnow() + timedelta(days=email_delay_days)).isoformat(),
        }

        logger.debug(f'POST {post_url}')
        logger.debug(post_data)

        return requests.post(post_url, post_data)
