from rest_framework import serializers

from common.models import ABSAEvent

class ABSAEventSerializer(serializers.ModelSerializer):
    class Meta:
        model               = ABSAEvent
        fields              = '__all__'
        read_only_fields    = [
            'created_at',
            'updated_at',
        ]
