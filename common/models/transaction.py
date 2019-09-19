from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import ObjectDoesNotExist
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from common.models import Inventory, Product, Vendor

class Transaction(BaseModel, models.Model):
    vendor                  = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    products                = models.ManyToManyField(Product)
    customer_email          = models.CharField(max_length=500, blank=True, null=True)
    customer_phone          = models.CharField(max_length=50, blank=True, null=True)
    review_requests_sent    = models.PositiveSmallIntegerField(default=0, help_text=_("The number of review requests we've sent to the customer regarding this transaction"))
    created_at              = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at              = models.DateTimeField(auto_now=True, editable=False)

    @property
    def customer_contact(self):
        return self.customer_email if self.customer_email else self.customer_phone

    def clean(self):
        if not self.customer_email and not self.customer_phone:
            raise ValidationError('At least one of `customer_email` and `customer_phone` must be set.')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.full_clean()
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def __str__(self):
        return f'[{str(self.created_at)[:19]}] {self.customer_contact}'

@receiver(m2m_changed, sender=Transaction.products.through)
def validate_vendor_product_relationship(sender, instance, **kwargs):
    for p in instance.products.all():
        try:
            inventory = Inventory.objects.get(vendor=instance.vendor, product=p)
        except ObjectDoesNotExist:
            raise Exception(f"Vendor {instance.vendor.name} doesn't have product {p} in inventory")
