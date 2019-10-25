from rest_framework import generics

from common.models import ABSAEvent, Review
from v1.serializers import ABSAEventSerializer, ReviewSerializer
# from ._auth import check_auth
from ._filters import ABSAEventFilter, ReviewFilter

class ReviewList(generics.ListCreateAPIView):
    """All reviews"""
    # queryset            = Review.objects.all()
    serializer_class    = ReviewSerializer
    filterset_class     = ReviewFilter

    def get_queryset(self):
        print('USER')
        print(self.request.user)
        print('AUTH')
        print(self.request.auth)
        return Review.objects.all()

class ReviewDetail(generics.RetrieveAPIView):
    """A specific review"""
    queryset            = Review.objects.all()
    serializer_class    = ReviewSerializer

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
