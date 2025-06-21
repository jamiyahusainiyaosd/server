from rest_framework import serializers
from .models import StudentResults, StudentResultImage

class StudentResultImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentResultImage
        fields = ['id', 'resultsSheetImg']

class StudentResueltsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentResults
        fields = ['id', 'studentClassName', 'resultCreatedAt', 'resultUpdatedAt']  

class StudentResueltsDetailSerializer(serializers.ModelSerializer):
    images = StudentResultImageSerializer(many=True, read_only=True)
    latest_update = serializers.SerializerMethodField()

    class Meta:
        model = StudentResults
        fields = ['id', 'studentClassName', 'studentClassDescription', 
                 'resultCreatedAt', 'resultUpdatedAt', 'images', 'latest_update']

    def get_latest_update(self, obj):
        if obj.images.exists():
            return obj.images.latest('resultSheetUpdatedAt').resultSheetUpdatedAt
        return None