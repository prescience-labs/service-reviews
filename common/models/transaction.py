from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from common.models import Product

class Transaction(BaseModel, models.Model):
    customer_email  = models.CharField(max_length=500, blank=True, null=True)
    customer_phone  = models.CharField(max_length=50, blank=True, null=True)
    products        = models.ManyToManyField(Product)
    created_at      = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at      = models.DateTimeField(auto_now=True, editable=False)

    @property
    def customer_contact(self):
        return self.customer_email if self.customer_email else self.customer_phone

    def clean(self):
        if self.customer_email is None and self.customer_phone is None:
            raise ValidationError('At least one of `customer_email` and `customer_phone` must be set.')

    def __str__(self):
        return f'[{str(self.created_at)[:19]}] {self.customer_contact}'
