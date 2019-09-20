from django.core.exceptions import ValidationError
from rest_framework import serializers

from common.models import Product, Transaction, Vendor

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model               = Transaction
        fields              = [
            'id',
            'vendor',
            'vendor_transaction_id',
            'customer_email',
            'customer_phone',
            'products',
            'created_at',
            'updated_at',
        ]
        read_only_fields    = [
            'id',
            'created_at',
            'updated_at',
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except ValidationError as e:
            message = 'The input was not valid. Please check your input and try again.'
            if type(e.messages) is list:
                message = e.messages[0]
            raise serializers.ValidationError(message)
class TransactionProductSerializer(serializers.ModelSerializer):
    class Meta:
        model               = Product
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

class UpsertTransactionComprehensiveSerializer(serializers.ModelSerializer):
    """Allows creating a transaction without knowledge of product or vendor IDs"""
    customer_email              = serializers.EmailField(required=False)
    vendor_integrations_type    = serializers.CharField(write_only=True)
    vendor_integrations_id      = serializers.CharField(write_only=True)
    vendor_product_ids          = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False,
        write_only=True,
    )

    class Meta:
        model               = Transaction
        fields              = [
            'id',
            'vendor',
            'vendor_transaction_id',
            'customer_email',
            'customer_phone',
            'created_at',
            'updated_at',
            'vendor_integrations_type',
            'vendor_integrations_id',
            'vendor_product_ids',
        ]
        read_only_fields    = [
            'id',
            'vendor',
            'created_at',
            'updated_at',
        ]

    def save(self):
        try:
            if not self.validated_data.get('customer_phone', None) and not self.validated_data.get('customer_email', None):
                raise serializers.ValidationError('At least one of `customer_phone` and `customer_email` must have a value.')

            vendor = Vendor.objects.get_or_none(
                integrations_type=self.validated_data.get('vendor_integrations_type', None),
                integrations_id=self.validated_data.get('vendor_integrations_id', None),
            )
            if not vendor:
                raise serializers.ValidationError(f"A vendor with `integrations_type` of `{self.validated_data.get('vendor_integrations_type', 'MISSING')}` and `integrations_id` of `{self.validated_data.get('vendor_integrations_id', 'MISSING')}` could not be found.")

            products = []
            for product_id in self.validated_data.get('vendor_product_ids', []):
                product = Product.objects.get_or_none(
                    inventory__vendor_product_id=product_id,
                    inventory__vendor=vendor,
                )
                if not product:
                    raise serializers.ValidationError(f"A product with `vendor_product_id` of `{product_id}` under the given vendor could not be found.")
                products.append(product)

            transaction = Transaction.objects.update_or_create(
                vendor__id=vendor.id,
                vendor_transaction_id=self.validated_data.get('vendor_transaction_id', None),
                defaults={
                    'vendor': vendor,
                    'vendor_transaction_id': self.validated_data.get('vendor_transaction_id', None),
                    'customer_email': self.validated_data.get('customer_email', None),
                    'customer_phone': self.validated_data.get('customer_phone', None),
                },
            )
            # update_or_create returns a tuple of (transaction, created=True/False)
            created = transaction[1]
            transaction = transaction[0]

            for p in products:
                transaction.products.add(p)
            return transaction
        except ValidationError as error:
            error_message = "The request wasn't formatted properly. Please check the body content and try again."
            if type(dict(error)['__all__']) is list: # find the error message for weird validation error
                error_message = dict(error)['__all__'][0]
            raise serializers.ValidationError(error_message)
        except serializers.ValidationError as error:
            raise serializers.ValidationError(error.detail)
        except:
            raise serializers.ValidationError('Something went terribly wrong :(', 500)
