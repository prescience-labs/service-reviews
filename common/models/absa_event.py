from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from ._base import BaseModel
from .review import Review

class ABSAEvent(BaseModel):
    ASPECT  = 'aspect'
    OPINION = 'opinion'

    TYPE_CHOICES = [
        (ASPECT, 'aspect'),
        (OPINION, 'opinion'),
    ]

    term        = models.CharField(max_length=255, help_text=_('The global term (e.g. "staff")'))
    variant     = models.CharField(max_length=255, help_text=_('The local variant of the term (e.g. "receptionist")'))
    start       = models.PositiveIntegerField(blank=True, null=True, help_text=_('The start position of the variant in the text'))
    end         = models.PositiveIntegerField(blank=True, null=True, help_text=_('The end position of the variant in the text'))
    event_type  = models.CharField(max_length=40, choices=TYPE_CHOICES)
    score       = models.FloatField(
        validators=[MinValueValidator(-1), MaxValueValidator(1)],
        help_text=_('The polarity score between -1 and 1'),
    )
    review      = models.ForeignKey(Review, on_delete=models.CASCADE)
    team_id     = models.CharField(max_length=255, help_text=_('The ID of the team that owns this event'))

    def __str__(self):
        return f'{self.term} ({self.variant})'
