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
    serializer_class    = VendorSerializer
    filterset_class     = VendorFilter

    def get_queryset(self):
        product_id = self.kwargs['pk']
        return Vendor.objects.filter(product__id=product_id)

    def create(self, request, pk, *args, **kwargs):
        """Creates a vendor with the product in their inventory.

        TODO: Add tests

        TODO: This has lots of logic that should ultimately live in a serializer.
        """
        product = Product.objects.get_or_none(pk=pk)
        if not product:
            raise serializers.ValidationError(f'A product with ID {pk} could not be found.', code=status.HTTP_404_NOT_FOUND)
        vendor_product_id = request.data.get('vendor_product_id', None)
        if not vendor_product_id: # this should be in a serializer in the future.
            raise serializers.ValidationError({'vendor_product_id':['This field is required.']})
        result = super().create(request, *args, **kwargs)
        vendor = Vendor.objects.get(pk=result.data['id']) # can't get it returned from self.create()
        inventory = Inventory.objects.create(product=product, vendor=vendor, vendor_product_id=vendor_product_id)
        return result
