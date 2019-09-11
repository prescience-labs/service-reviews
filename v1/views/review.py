from rest_framework import generics

from common.models import Review
from v1.serializers import ReviewSerializer

class ReviewList(generics.ListCreateAPIView):
    queryset            = Review.objects.all()
    serializer_class    = ReviewSerializer

class ReviewDetail(generics.RetrieveAPIView):
    queryset            = Review.objects.all()
    serializer_class    = ReviewSerializer
