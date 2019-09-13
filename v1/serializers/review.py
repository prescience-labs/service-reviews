from rest_framework import serializers

from common.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model               = Review
        fields              = [
            'id',
            'text',
            'rating',
            'rating_max',
            'sentiment_analysis',
            'created_at',
            'updated_at',
        ]
        read_only_fields    = [
            'sentiment_analysis',
            'created_at',
            'updated_at',
        ]
