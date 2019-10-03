from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel

class Vendor(BaseModel, models.Model):
    name                    = models.CharField(max_length=255)
    integrations_type       = models.CharField(max_length=1000, blank=True, null=True, help_text=_('Set by the integrations service to uniquely identify a vendor'))
    integrations_id         = models.CharField(max_length=1000, blank=True, null=True, help_text=_('Set by the integrations service to uniquely identify a vendor'))
    send_comms_to_customers = models.BooleanField(default=False, help_text=_("A flag for sending texts, emails, etc to this vendor's customers (e.g. review requests)"))
    created_at              = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at              = models.DateTimeField(auto_now=True, editable=False)

    @property
    def products(self):
        """Return the queryset of products belonging to the vendor instance."""
        return self.product_set.all()

    class Meta:
        unique_together = [
            ['integrations_type', 'integrations_id'],
        ]

    def __str__(self):
        return f'{self.name} ({str(self.id)[-5:]})'
