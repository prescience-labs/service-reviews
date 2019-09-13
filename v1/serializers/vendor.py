from rest_framework import serializers

from common.models import Product, Vendor

class VendorSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model               = Vendor
        fields              = [
            'id',
            'name',
            'products',
            'created_at',
            'updated_at',
        ]
        read_only_fields    = [
            'id',
            'created_at',
            'updated_at',
        ]
