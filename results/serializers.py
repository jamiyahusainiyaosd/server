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

    class Meta:
        model = StudentResults
        fields = ['id', 'studentClassName', 'studentClassDescription', 'resultCreatedAt', 'resultUpdatedAt', 'images']