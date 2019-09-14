from rest_framework import serializers

from common.models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )

    class Meta:
        model               = Transaction
        fields              = [
            'id',
            'vendor',
            'customer_email',
            'customer_phone',
            'products',
            'created_at',
            'updated_at',
        ]
        read_only_fields    = [
            'id',
            'created_at',
            'updated_at',
        ]
