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

    def create(self, validated_data):
        """Creates a product and connects it with the vendor."""
        vendor_id   = self.context['vendor_id'] if self.context['vendor_id'] else None
        if vendor_id is not None:
            vendor      = Vendor.objects.get(pk=vendor_id)
            product     = Product.objects.create(validated_data)
            inventory   = Inventory(
                vendor=vendor,
                product=product,
                vendor_product_id=validated_data['vendor_product_id'],
            )
            inventory.save()
            return product


class VendorProductSerializer(serializers.ModelSerializer):
    vendor_product_id = serializers.UUIDField(source='*')

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

class RetrieveVendorProductSerializer(VendorProductSerializer):
    vendor_product_id = serializers.SerializerMethodField()

    def get_vendor_product_id(self, obj):
        """Returns the vendor_product_id of the product given the vendor from the context.

        This relies on a `vendor_id` being passed in the context.

        Returns:
            string: The vendor-product identifier
        """
        vendor_id   = self.context['vendor_id'] if self.context['vendor_id'] else None
        item        = Inventory.objects.get(vendor__id=vendor_id, product=obj)
        print(item)
        return item.vendor_product_id
