from rest_framework import serializers

from common.models import Product, Vendor

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model               = Vendor
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
