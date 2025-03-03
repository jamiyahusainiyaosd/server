from rest_framework import serializers
from .models import Notice

class NoticeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields =  ['id', 'title', 'created_at']

class NoticeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id', 'title', 'description', 'created_at', 'updated_at']