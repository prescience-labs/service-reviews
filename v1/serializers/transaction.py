from rest_framework import serializers

from common.models import Product, Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model               = Transaction
        fields              = [
            'id',
            'vendor',
            'customer_email',
            'customer_phone',
            'created_at',
            'updated_at',
        ]
        read_only_fields    = [
            'id',
            'created_at',
            'updated_at',
        ]
class TransactionProductSerializer(serializers.ModelSerializer):
    class Meta:
        model               = Product
        fields              = [
            'id',
            'name',
            'created_at',
            'updated_at',
        ]
        read_only_fields    = [
            'id',
            'created_at',
            'updated_at',
        ]
