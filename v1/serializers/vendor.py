from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.models import Inventory, Product, Vendor

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model               = Vendor
        fields              = [
            'id',
            'name',
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

class VendorProductSerializer(serializers.ModelSerializer):
    vendor_product_id = serializers.CharField()

    class Meta:
        model               = Product
        fields              = [
            'id',
            'name',
            'vendor_product_id',
            'created_at',
            'updated_at',
        ]
        read_only_fields    = [
            'id',
            'created_at',
            'updated_at',
        ]

    def save(self):
        vendor_id   = self.context['vendor_id'] if self.context['vendor_id'] else None
        vendor      = Vendor.objects.get(pk=vendor_id)
        product     = Product.objects.create(name=self.validated_data['name'])
        inventory   = Inventory.objects.create(vendor=vendor, product=product, vendor_product_id=self.validated_data['vendor_product_id'])
        return product

class RetrieveVendorProductSerializer(VendorProductSerializer):
    vendor_product_id = serializers.SerializerMethodField(help_text=_("A value representing the vendor's ID number for the product."))

    def get_vendor_product_id(self, obj):
        """Returns the vendor_product_id of the product given the vendor from the context.

        This relies on a `vendor_id` being passed in the context.

        Returns:
            string: The vendor-product identifier
        """
        vendor_id   = self.context['vendor_id'] if self.context['vendor_id'] else None
        item        = Inventory.objects.get(vendor__id=vendor_id, product=obj)
        return item.vendor_product_id
