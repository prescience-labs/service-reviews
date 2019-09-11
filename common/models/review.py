from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel

class Review(BaseModel, models.Model):
    text                = models.TextField()
    source              = models.CharField(max_length=255, help_text=_('The source of the review (e.g. Google, Shopify, Amazon)'))
    rating              = models.PositiveSmallIntegerField(blank=True, null=True, help_text=_('The review rating, if it was included'))
    rating_max          = models.PositiveSmallIntegerField(blank=True, null=True, help_text=_('The max possible review rating, if it was included'))
    analytics_id        = models.UUIDField(blank=True, null=True, help_text=_(f'The document id from the documents service ({settings.DOCUMENT_SERVICE_BASE_URL})'))
    sentiment_analysis  = JSONField(blank=True, null=True, help_text=_('The sentiment analysis from the document service'))
    created_at          = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at          = models.DateTimeField(auto_now=True, editable=False)
