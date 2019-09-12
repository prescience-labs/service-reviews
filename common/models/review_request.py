from datetime import datetime

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel, Review

class ReviewRequest(BaseModel, models.Model):
    target_customer_email   = models.CharField(max_length=500, blank=True, null=True)
    target_customer_phone   = models.CharField(max_length=50, blank=True, null=True)
    product_name            = models.CharField(max_length=500)
    review                  = models.OneToOneField(Review, on_delete=models.CASCADE, blank=True, null=True)
    created_at              = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at              = models.DateTimeField(auto_now=True, editable=False)

@receiver(pre_save, sender=ReviewRequest)
def check_target_customer_info(sender, instance, **kwargs):
    """Throws an error if both target_customer_email and target_customer_phone are blank.

    In order to know where and how to send a review request to a customer, we
    need access to some contact information.
    """
    if instance.target_customer_email is None and instance.target_customer_phone is None:
        raise ValidationError('At least one of `target_customer_email` and `target_customer_phone` must be set.')
