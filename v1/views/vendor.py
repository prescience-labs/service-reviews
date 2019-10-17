from django.db import IntegrityError
from django_filters import rest_framework as filters
from rest_framework import generics, serializers, status
from rest_framework.response import Response

from common.models import Inventory, Product, Vendor
from v1.serializers import (
    ProductSerializer,
    VendorSerializer,
    VendorProductSerializer,
)
from ._filters import ProductFilter, VendorFilter

class VendorList(generics.ListCreateAPIView):
    """All vendors"""
    queryset            = Vendor.objects.all()
    serializer_class    = VendorSerializer
    filterset_class     = VendorFilter

class VendorDetail(generics.RetrieveUpdateAPIView):
    """A specific vendor"""
    queryset            = Vendor.objects.all()
    serializer_class    = VendorSerializer

class VendorProductList(generics.ListCreateAPIView):
    """A specific vendor's products"""
    serializer_class    = VendorProductSerializer
    filterset_class     = ProductFilter

    def get_queryset(self):
        vendor_id = self.kwargs['pk']
        return Product.objects.filter(vendors__id=vendor_id)

    def get_serializer_context(self):
        return {
            'request': self.request,
            'vendor_id': self.kwargs['pk'],
        }
