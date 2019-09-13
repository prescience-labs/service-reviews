from rest_framework import generics

from common.models import Product
from v1.serializers import ProductSerializer

class ProductList(generics.ListCreateAPIView):
    queryset            = Product.objects.all()
    serializer_class    = ProductSerializer

class ProductDetail(generics.RetrieveAPIView):
    queryset            = Product.objects.all()
    serializer_class    = ProductSerializer
