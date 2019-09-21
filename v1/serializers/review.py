from rest_framework import serializers

from common.models import Review

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
            'created_at',
            'updated_at',
        ]
