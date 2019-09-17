from django.db import models
from django.db.models import ObjectDoesNotExist

class GetOrNoneManager(models.Manager):
    def get_or_none(self, **kwargs):
        """Returns the object if it exists or None if it doesn't"""
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None
