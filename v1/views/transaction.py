from rest_framework import generics
from rest_framework.response import Response

from common.models import Product, Transaction
from v1.serializers import TransactionProductSerializer, TransactionSerializer

class TransactionList(generics.ListCreateAPIView):
    queryset            = Transaction.objects.all()
    serializer_class    = TransactionSerializer

class TransactionDetail(generics.RetrieveAPIView):
    queryset            = Transaction.objects.all()
    serializer_class    = TransactionSerializer

class TransactionProductList(generics.ListAPIView):
    queryset            = Product.objects.all()
    serializer_class    = TransactionProductSerializer

    def list(self, request, pk):
        queryset    = Product.objects.filter(transaction__id=pk)
        serializer  = TransactionProductSerializer(queryset, many=True, context={'vendor_id': pk})
        return Response(serializer.data)
