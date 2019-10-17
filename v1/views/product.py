from django_filters import rest_framework as filters
from rest_framework import generics, serializers, status
from rest_framework.response import Response

from common.models import Inventory, Product, Vendor
from v1.serializers import (
    ProductSerializer,
    ProductVendorSerializer,
    VendorSerializer,
)
from ._filters import ProductFilter, VendorFilter

class ProductList(generics.ListCreateAPIView):
    """All products"""
    queryset            = Product.objects.all()
    serializer_class    = ProductSerializer
    filterset_class     = ProductFilter

class ProductDetail(generics.RetrieveUpdateAPIView):
    """A specific product"""
    queryset            = Product.objects.all()
    serializer_class    = ProductSerializer

class ProductVendorList(generics.ListCreateAPIView):
    """The vendors for a specific product"""
    serializer_class    = ProductVendorSerializer
    filterset_class     = VendorFilter

    def get_queryset(self):
        product_id = self.kwargs['pk']
        return Vendor.objects.filter(product__id=product_id)

    def get_serializer_context(self):
        return {
            'request': self.request,
            'product_id': self.kwargs['pk'],
        }
