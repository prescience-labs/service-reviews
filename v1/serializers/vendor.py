from rest_framework import serializers

from common.models import Product, Vendor

class VendorSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, queryset=Product.objects.all())

    class Meta:
        model               = Vendor
        fields              = [
            'id',
            'name',
            'integrations_type',
            'integrations_id',
            'products',
            'created_at',
            'updated_at',
        ]
        read_only_fields    = [
            'id',
            'created_at',
            'updated_at',
        ]
        filterset_fields = ['integrations_type', 'integrations_id']
