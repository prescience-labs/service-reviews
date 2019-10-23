from rest_framework import generics

from common.models import ABSAEvent
from v1.serializers import ABSAEventSerializer
from ._filters import ABSAEventFilter

class ABSAEventList(generics.ListAPIView):
    queryset            = ABSAEvent.objects.all()
    serializer_class    = ABSAEventSerializer
    filterset_class     = ABSAEventFilter
