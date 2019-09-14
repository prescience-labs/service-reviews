from rest_framework import serializers

from common.models import Product, Vendor

class ProductSerializer(serializers.ModelSerializer):
    vendors = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Vendor.objects.all(),
        required=False,
    )

    class Meta:
        model               = Product
        fields              = [
            'id',
            'name',
            'vendors',
            'created_at',
            'updated_at',
        ]
        read_only_fields    = [
            'id',
            'created_at',
            'updated_at',
        ]