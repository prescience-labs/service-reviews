from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel, Product, Vendor

class Inventory(BaseModel, models.Model):
    """The many-to-many connection between Vendor and Products.

    A Vendor can sell multiple products, and each product can be sold by
    multiple vendors. That relationship has additional information, such
    as the vendor-specific product ID.
    """
    vendor_product_id   = models.CharField(max_length=255, help_text=_('The vendor-specific product ID'))
    product             = models.ForeignKey(Product, on_delete=models.CASCADE)
    vendor              = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    created_at          = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at          = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f'{self.vendor.name}: {self.product.name} (ID: {self.vendor_product_id})'
