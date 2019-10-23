from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from ._base import BaseModel
from .vendor import Vendor

class Product(BaseModel):
    name        = models.CharField(max_length=255)
    team_id     = models.CharField(max_length=255, help_text=_('The ID of the team that owns this product'))
    vendors     = models.ManyToManyField(Vendor, through='Inventory')

    def __str__(self):
        return f'{self.name} ({str(self.id)[-5:]})'
