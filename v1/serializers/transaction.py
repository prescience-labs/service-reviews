from django.core.exceptions import ValidationError
from rest_framework import serializers

from common.models import Product, Transaction, Vendor

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model               = Transaction
        fields              = [
            'id',
            'vendor',
            'customer_email',
            'customer_phone',
            'created_at',
            'updated_at',
        ]
        read_only_fields    = [
            'id',
            'created_at',
            'updated_at',
        ]
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

class CreateTransactionComprehensiveSerializer(serializers.ModelSerializer):
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

            vendor = Vendor.objects.get(
                integrations_type=self.validated_data.get('vendor_integrations_type', None),
                integrations_id=self.validated_data.get('vendor_integrations_id', None),
            )
            products = []
            for product_id in self.validated_data.get('vendor_product_ids', []):
                products.append(Product.objects.get(
                    inventory__vendor_product_id=product_id,
                    inventory__vendor=vendor,
                ))
            transaction = Transaction.objects.create(
                vendor=vendor,
                customer_email=self.validated_data.get('customer_email', None),
                customer_phone=self.validated_data.get('customer_phone', None),
            )
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
