from rest_framework import serializers

from common.models import Product, Review, Transaction

class ReviewSerializer(serializers.ModelSerializer):
    # Must set default=None on these because they are part of a unique_together constraint
    # https://github.com/encode/django-rest-framework/issues/4456#issuecomment-244017057
    product     = serializers.CharField(required=False, allow_null=True, default=None)
    transaction = serializers.CharField(required=False, allow_null=True, default=None)

    class Meta:
        model               = Review
        fields              = '__all__'
        read_only_fields    = [
            'sentiment_analysis',
            'analytics_id',
            'created_at',
            'updated_at',
        ]

    def create(self, validated_data):
        # Fix issue where creating a review for a product when passing in just a product ID
        # errors. We need to use that product id to find the product.
        validated_data['transaction']   = Transaction.objects.get_or_none(pk=validated_data['transaction'])if validated_data['transaction'] else None
        validated_data['product']       = Product.objects.get_or_none(pk=validated_data['product']) if validated_data['product'] else None
        return super().create(validated_data)
