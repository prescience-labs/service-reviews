from rest_framework import serializers

from common.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    product     = serializers.UUIDField(required=False, allow_null=True, allow_blank=True)
    transaction = serializers.UUIDField(required=False, allow_null=True, allow_blank=True)
    class Meta:
        model               = Review
        fields              = '__all__'
        read_only_fields    = [
            'sentiment_analysis',
            'created_at',
            'updated_at',
        ]
