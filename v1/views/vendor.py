from rest_framework import generics, status
from rest_framework.response import Response

from common.models import Product, Vendor
from v1.serializers import (
    ProductSerializer,
    VendorSerializer,
    VendorProductSerializer,
    RetrieveVendorProductSerializer,
)

class VendorList(generics.ListCreateAPIView):
    queryset            = Vendor.objects.all()
    serializer_class    = VendorSerializer
    filterset_fields    = ('integrations_type', 'integrations_id',)

class VendorDetail(generics.RetrieveAPIView):
    queryset            = Vendor.objects.all()
    serializer_class    = VendorSerializer

class VendorProductList(generics.ListCreateAPIView):
    queryset            = Product.objects.all()
    serializer_class    = ProductSerializer

    def list(self, request, pk):
        queryset    = Product.objects.filter(vendors__id=pk)
        serializer  = RetrieveVendorProductSerializer(queryset, many=True, context={'vendor_id': pk})
        return Response(serializer.data)

    def create(self, request, pk):
        serializer  = VendorProductSerializer(data=request.data, context={'vendor_id': pk})
        if serializer.is_valid():
            result = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED if result[1] else status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
