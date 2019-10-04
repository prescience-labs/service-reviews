from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.models import Inventory, Product, Vendor

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model               = Product
        fields              = '__all__'
        read_only_fields    = [
            'id',
            'created_at',
            'updated_at',
        ]

class ProductVendorSerializer(serializers.ModelSerializer):
    vendor_product_id = serializers.CharField()

    # Must set default=None on these because they are part of a unique_together constraint
    # https://github.com/encode/django-rest-framework/issues/4456#issuecomment-244017057
    integrations_type   = serializers.CharField(required=False, allow_null=True, default=None)
    integrations_id     = serializers.CharField(required=False, allow_null=True, default=None)

    class Meta:
        model               = Vendor
        fields              = [
            'id',
            'name',
            'team_id',
            'vendor_product_id',
            'integrations_type',
            'integrations_id',
            'created_at',
            'updated_at',
        ]
        read_only_fields    = [
            'id',
            'created_at',
            'updated_at',
        ]
