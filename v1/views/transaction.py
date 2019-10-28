from rest_framework import generics, status
from rest_framework.response import Response

from common.models import Product, Transaction
from v1.serializers import (
    TransactionProductSerializer,
    TransactionSerializer,
    UpsertTransactionComprehensiveSerializer,
)
from ._filters import TransactionFilter

class TransactionList(generics.ListCreateAPIView):
    """All transactions"""
    queryset            = Transaction.objects.all()
    serializer_class    = TransactionSerializer
    filterset_class     = TransactionFilter

class TransactionDetail(generics.RetrieveAPIView):
    """A specific transaction"""
    queryset            = Transaction.objects.all()
    serializer_class    = TransactionSerializer

class TransactionProductList(generics.ListAPIView):
    """All products that are related to the specified transaction"""
    queryset            = Product.objects.all()
    serializer_class    = TransactionProductSerializer

    def list(self, request, pk):
        queryset    = Product.objects.filter(transaction__id=pk)
        serializer  = TransactionProductSerializer(queryset, many=True, context={'vendor_id': pk})
        return Response(serializer.data)

class UpsertTransactionComprehensive(generics.CreateAPIView):
    """Allows creating/updating a transaction without knowledge of product or vendor IDs

    This POST request upserts (update or insert) the transaction.

    The user of this route must have knowledge of:
        - `integrations_type`
        - `integrations_id`
        - `vendor_product_id` (one or more)
        - `vendor_transaction_id`
    """
    serializer_class = UpsertTransactionComprehensiveSerializer

    def post(self, request):
        serializer  = UpsertTransactionComprehensiveSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED if result[1] else status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
