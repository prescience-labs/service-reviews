from rest_framework import generics

from common.models import Transaction
from v1.serializers import TransactionSerializer

class TransactionList(generics.ListCreateAPIView):
    queryset            = Transaction.objects.all()
    serializer_class    = TransactionSerializer

class TransactionDetail(generics.RetrieveAPIView):
    queryset            = Transaction.objects.all()
    serializer_class    = TransactionSerializer
