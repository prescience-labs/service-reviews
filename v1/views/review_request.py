from rest_framework import generics

from common.models import ReviewRequest
from v1.serializers import ReviewRequestSerializer

class ReviewRequestList(generics.ListCreateAPIView):
    queryset            = ReviewRequest.objects.all()
    serializer_class    = ReviewRequestSerializer

class ReviewRequestDetail(generics.RetrieveAPIView):
    queryset            = ReviewRequest.objects.all()
    serializer_class    = ReviewRequestSerializer
