from rest_framework import generics

from common.models import ABSAEvent
from v1.serializers import ABSAEventSerializer
from ._filters import ABSAEventFilter

class ABSAEventList(generics.ListAPIView):
    serializer_class    = ABSAEventSerializer
    filterset_class     = ABSAEventFilter

    def get_queryset(self):
        if self.request.auth == 'user':
            return ABSAEvent.objects.filter(team_id=self.request.user.get('active_team'))
        elif self.request.auth == 'client':
            return ABSAEvent.objects.all()
