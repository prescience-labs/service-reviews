from rest_framework import generics

from common.models import Vendor
from v1.serializers import VendorSerializer

class VendorList(generics.ListCreateAPIView):
    queryset            = Vendor.objects.all()
    serializer_class    = VendorSerializer
    filterset_fields    = ('integrations_type', 'integrations_id',)

class VendorDetail(generics.RetrieveAPIView):
    queryset            = Vendor.objects.all()
    serializer_class    = VendorSerializer