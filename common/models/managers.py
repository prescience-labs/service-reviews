from django.db import models
from django.db.models import ObjectDoesNotExist

class GetOrNoneManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None
