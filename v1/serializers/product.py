import logging

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.models import Inventory, Product, Vendor

logger = logging.getLogger(__name__)

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
    vendor_product_id = serializers.CharField(help_text=_("A value representing the vendor's ID number for the product."), write_only=True)

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
            'team_id',
            'created_at',
            'updated_at',
        ]

    def create(self, validated_data):
        try:
            logger.debug(f'Validated data: {validated_data}')
            product_id  = self.context.get('product_id', None)
            product     = Product.objects.get_or_none(pk=product_id)
            if not product:
                raise serializers.ValidationError(f"A product with id {product_id} could not be found.")

            logger.debug(product.team_id)
            vendor_product_id = validated_data.get('vendor_product_id', None)
            if not vendor_product_id:
                raise serializers.ValidationError("Somehow the `vendor_product_id` wasn't included in the request. Try adding that in the body.")

            vendor      = Vendor.objects.create(
                name=validated_data['name'],
                team_id=product.team_id,
                integrations_type=validated_data.get('integrations_type', None),
                integrations_id=validated_data.get('integrations_id', None),
            )
            inventory   = Inventory.objects.create(product=product, vendor=vendor, vendor_product_id=vendor_product_id)
            return vendor
        except serializers.ValidationError as error:
            raise serializers.ValidationError(error.detail)
        except:
            raise serializers.ValidationError("We weren't able to fulfill this request. Please try it again. If this keeps happening, give us a call.", code=500)
