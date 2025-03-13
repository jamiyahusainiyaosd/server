from rest_framework import serializers
from .models import PhotoGallary, VideoGallary

class PhotoGallarySerializers(serializers.ModelSerializer):
    class Meta:
        model = PhotoGallary
        fields = ['id', 'photoTitle', 'photoImg']

class VideoGallarySerializers(serializers.ModelSerializer):
    class Meta:
        model = VideoGallary
        fields = ['id', 'videoTitle', 'videoImg']