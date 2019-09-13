from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel

class Vendor(BaseModel, models.Model):
    name        = models.CharField(max_length=255)
    created_at  = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at  = models.DateTimeField(auto_now=True, editable=False)

    @property
    def products(self):
        """Return the queryset of products belonging to the vendor instance."""
        return self.product_set.all()

    def __str__(self):
        return f'{self.name} ({str(self.id)[-5:]})'
