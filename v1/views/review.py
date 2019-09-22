from rest_framework import generics

from common.models import Review
from v1.serializers import ReviewSerializer
from ._filters import ReviewFilter

class ReviewList(generics.ListCreateAPIView):
    queryset            = Review.objects.all()
    serializer_class    = ReviewSerializer
    filterset_class     = ReviewFilter

class ReviewDetail(generics.RetrieveAPIView):
    queryset            = Review.objects.all()
    serializer_class    = ReviewSerializer
