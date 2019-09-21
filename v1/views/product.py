from django_filters import rest_framework as filters
from rest_framework import generics, status
from rest_framework.response import Response

from common.models import Product, Vendor
from v1.serializers import (
    ProductSerializer,
    ProductVendorSerializer,
    RetrieveProductVendorSerializer,
    VendorSerializer,
)

class ProductFilter(filters.FilterSet):
    vendor_product_id = filters.CharFilter(field_name='inventory__vendor_product_id')

    class Meta:
        model   = Product
        fields  = ['name', 'vendor_product_id']

class ProductList(generics.ListCreateAPIView):
    queryset            = Product.objects.all()
    serializer_class    = ProductSerializer
    filterset_class     = ProductFilter

class ProductDetail(generics.RetrieveUpdateAPIView):
    queryset            = Product.objects.all()
    serializer_class    = ProductSerializer

class ProductVendorList(generics.ListCreateAPIView):
    queryset            = Vendor.objects.all()
    serializer_class    = VendorSerializer

    def list(self, request, pk):
        queryset    = Vendor.objects.filter(product__id=pk)
        serializer  = RetrieveProductVendorSerializer(queryset, many=True, context={'product_id': pk})
        return Response(serializer.data)

    def create(self, request, pk):
        serializer  = ProductVendorSerializer(data=request.data, context={'product_id': pk})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
