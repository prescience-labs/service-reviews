from django_filters import rest_framework as filters
from rest_framework import generics, serializers, status
from rest_framework.response import Response

from common.models import Inventory, Product, Vendor
from v1.serializers import (
    ProductSerializer,
    VendorSerializer,
    VendorProductSerializer,
    RetrieveVendorProductSerializer,
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
    serializer_class    = ProductSerializer
    filterset_class     = ProductFilter

    def get_queryset(self):
        vendor_id = self.kwargs['pk']
        return Product.objects.filter(vendors__id=vendor_id)

    def create(self, request, pk, *args, **kwargs):
        """Creates a product and puts it in the vendor's inventory.

        TODO: This has lots of logic that should ultimately live in a serializer.
        """
        vendor = Vendor.objects.get(pk=pk)
        vendor_product_id = request.data.get('vendor_product_id', None)
        if not vendor_product_id: # this should be in a serializer in the future.
            raise serializers.ValidationError({'vendor_product_id':['This field is required.']})
        result = super().create(request, *args, **kwargs)
        product = Product.objects.get(pk=result.data['id']) # can't get it returned from self.create()
        inventory = Inventory.objects.create(product=product, vendor=vendor, vendor_product_id=vendor_product_id)
        return result
