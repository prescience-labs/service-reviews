import logging

from django.conf import settings
from django.db import IntegrityError
from django.db.models import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
import requests
from rest_framework import serializers

from common.models import Inventory, Product, Vendor

logger = logging.getLogger(__name__)

class VendorSerializer(serializers.ModelSerializer):
    # Must set default=None on these because they are part of a unique_together constraint
    # https://github.com/encode/django-rest-framework/issues/4456#issuecomment-244017057
    integrations_type   = serializers.CharField(required=False, allow_null=True, default=None)
    integrations_id     = serializers.CharField(required=False, allow_null=True, default=None)
    team_id             = serializers.CharField(required=False, default=None)

    class Meta:
        model               = Vendor
        fields              = '__all__'
        read_only_fields    = [
            'id',
            'created_at',
            'updated_at',
        ]

    def create(self, validated_data):
        team_id = validated_data.get('team_id', None)
        team    = None
        if team_id:
            logger.debug(f"team_id {team_id} included in the request; checking if it is a valid team")
            team = requests.get(f"{settings.AUTH_SERVICE['BASE_URL']}/teams/{team_id}")
        if not team_id or not team:
            logger.debug(f"team_id: {team_id}; team: {team}")
            logger.debug('Team not found. Creating a new team for this vendor.')
            response = requests.post(f"{settings.AUTH_SERVICE['BASE_URL']}/teams",
                json={
                    'name': f"{validated_data['name']}'s Team",
                },
            )
            team_id = response.json()['id']
        validated_data['team_id'] = team_id
        logger.debug(f'Creating a vendor: {validated_data}')
        vendor = super().create(validated_data)
        return vendor

class VendorProductSerializer(serializers.ModelSerializer):
    vendor_product_id = serializers.SerializerMethodField(help_text=_("A value representing the vendor's ID number for the product."))

    class Meta:
        model               = Product
        fields              = [
            'id',
            'name',
            'team_id',
            'vendor_product_id',
            'created_at',
            'updated_at',
        ]
        read_only_fields    = [
            'id',
            'created_at',
            'updated_at',
        ]

    def get_vendor_product_id(self, obj):
        """Returns the vendor_product_id of the product given the vendor from the context.

        This relies on a `vendor_id` being passed in the context.

        Returns:
            string: The vendor-product identifier
        """
        print(self.args)
        print(self.request.args)
        vendor_id   = self.context['vendor_id'] if self.context['vendor_id'] else None
        item        = Inventory.objects.get(vendor__id=vendor_id, product=obj)
        return item.vendor_product_id

    def create(self, validated_data):
        return super().create(validated_data)
