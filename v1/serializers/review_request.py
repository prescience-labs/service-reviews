from rest_framework import serializers

from common.models import ReviewRequest

class ReviewRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model               = ReviewRequest
        fields              = [
            'id',
            'target_customer_email',
            'target_customer_phone',
            'product_name',
            'is_thumbs_up',
            'review_text',
            'review_completed_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields    = [
            'review_completed_at',
            'created_at',
            'updated_at',
        ]
