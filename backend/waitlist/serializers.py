from rest_framework import serializers
from .models import WaitlistUser

class WaitlistUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaitlistUser
        fields = ['email', 'source']
        
    def create(self, validated_data):
        return WaitlistUser.objects.create(**validated_data)
