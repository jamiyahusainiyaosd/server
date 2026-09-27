from rest_framework import serializers
from .models import Notice, Announcement

class NoticeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id', 'title', 'created_at']

class NoticeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id', 'title', 'description', 'created_at', 'updated_at']

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'text', 'order', 'is_active', 'created_at']
