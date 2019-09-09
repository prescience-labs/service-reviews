import uuid
from django.db import models

class BaseModel(models.Model):
    """The base model from which all other models inherit."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
