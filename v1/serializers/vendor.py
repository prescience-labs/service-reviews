from django.db import IntegrityError
from django.db.models import ObjectDoesNotExist
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

    def is_valid(self, raise_exception=False):
        """Validates the input

        For this specific implementation, we are using the data to do an
        upsert on Vendor, so we have to check that the unique constraint
        is there but we aren't violating it. This is ok because we also
        run the unique constraint on the model itself before it saves to
        the database.

        Args:
            raise_exception (bool, optional): Raise an exception if it fails. Defaults to False.

        Returns:
            boolean: Is the serializer data valid
        """
        result = super().is_valid(raise_exception=raise_exception)
        if not result:
            if 'non_field_errors' in self.errors:
                for e in self.errors['non_field_errors']:
                    if 'integrations_type' in e and e.code == 'unique':
                        result = True
        return result

    def create(self, validated_data):
        result = Vendor.objects.update_or_create(
            integrations_type=validated_data.get('integrations_type', None),
            integrations_id=validated_data.get('integrations_id', None),
            defaults={
                'name': validated_data.get('name', None)
            },
        )
        print(result[0])
        return result

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
        """Upserts a product

        Returns a tuple that contains the product itself and a boolean value
        that is True if the object was created in the database and false if not.

        Returns:
            tuple: (product object, created boolean)
        """
        vendor_id   = self.context['vendor_id']
        vendor      = Vendor.objects.get(pk=vendor_id)
        if not vendor:
            raise serializers.ValidationError(f'Vendor with id {vendor_id} does not exist')

        # we do update_or_create to allow the integrations service to POST to the endpoint
        # without doing additional checks to see if the object already exists
        product     = Product.objects.update_or_create(
            inventory__vendor_product_id=self.validated_data.get('vendor_product_id', None),
            inventory__vendor=vendor,
            defaults={'name': self.validated_data.get('name', None)}
        )

        created     = product[1]
        product     = product[0] # update_or_create returns a tuple, first object is product
        inventory   = Inventory.objects.get_or_create(vendor=vendor, product=product, vendor_product_id=self.validated_data.get('vendor_product_id'))

        return (product, created)

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
