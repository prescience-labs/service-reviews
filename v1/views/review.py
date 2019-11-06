from rest_framework import generics

from common.models import ABSAEvent, Review
from v1.serializers import ABSAEventSerializer, ReviewSerializer
# from ._auth import check_auth
from ._filters import ABSAEventFilter, ReviewFilter

class ReviewList(generics.ListCreateAPIView):
    serializer_class    = ReviewSerializer
    filterset_class     = ReviewFilter

    def get_queryset(self):
        if self.request.auth == 'user':
            return Review.objects.filter(vendor__team_id=self.request.user.get('active_team'))
        elif self.request.auth == 'client':
            return Review.objects.all()

class ReviewDetail(generics.RetrieveAPIView):
    serializer_class    = ReviewSerializer

    def get_queryset(self):
        if self.request.auth == 'user':
            return Review.objects.filter(vendor__team_id=self.request.user.get('active_team'))
        elif self.request.auth == 'client':
            return Review.objects.all()

class ReviewABSAEventList(generics.ListAPIView):
    serializer_class    = ABSAEventSerializer
    filterset_class     = ABSAEventFilter

    def get_queryset(self):
        review_id = self.kwargs['pk']
        return ABSAEvent.objects.filter(review__id=review_id)

    def get_serializer_context(self):
        return {
            'request': self.request,
            'review_id': self.kwargs['pk'],
        }
