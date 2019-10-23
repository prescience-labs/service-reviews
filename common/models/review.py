from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from ._base import BaseModel
from .inventory import Inventory
from .product import Product
from .transaction import Transaction
from .vendor import Vendor

class Review(BaseModel):
    """
    Review
        - MUST be associated with a Vendor
        - SHOULD be associated with a Product
        - SHOULD be associated with a Transaction
    """
    vendor              = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    product             = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, help_text=_('The product this review is about'))
    transaction         = models.ForeignKey(Transaction, on_delete=models.CASCADE, blank=True, null=True, help_text=_('The transaction associated with this review'))
    text                = models.TextField()
    rating              = models.PositiveSmallIntegerField(blank=True, null=True, help_text=_('The review rating, if it was included'))
    rating_max          = models.PositiveSmallIntegerField(blank=True, null=True, help_text=_('The max possible review rating, if it was included'))
    analytics_id        = models.UUIDField(blank=True, null=True, help_text=_(f'The document id from the <a href="{settings.DOCUMENTS_SERVICE["BASE_URL"]}">Documents Service</a>'))
    sentiment_analysis  = JSONField(blank=True, null=True, help_text=_('The sentiment analysis from the document service'))
    created_at          = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at          = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        unique_together = [
            ['transaction', 'product'],
        ]

    def clean(self):
        # Check that the product (if provided) was on the transaction (if provided)
        if self.transaction is not None and self.product is not None:
            if self.product not in self.transaction.products.all():
                raise ValidationError("That Product isn't on that Transaction")

        # Check that the product (if provided) can be tied to the vendor
        if self.product is not None:
            try:
                inventory = Inventory.objects.get(vendor=self.vendor, product=self.product)
            except ObjectDoesNotExist:
                raise ValidationError(f"Vendor {self.vendor} doesn't have product {self.product} in inventory")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.full_clean()
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
