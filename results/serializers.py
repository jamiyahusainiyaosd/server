from rest_framework import serializers
from .models import StudentResults, StudentResultImage, TopAchiever

class StudentResultImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentResultImage
        fields = ['id', 'resultsSheetImg']

class StudentResueltsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentResults
        fields = [
            'id', 'studentClassName', 'exam_session', 'academic_year', 
            'board_name', 'total_students', 'passed_students', 'pass_rate', 
            'grade_detail', 'certificate_status', 'helpline', 'resultCreatedAt', 'resultUpdatedAt'
        ]  

class StudentResueltsDetailSerializer(serializers.ModelSerializer):
    images = StudentResultImageSerializer(many=True, read_only=True)
    latest_update = serializers.SerializerMethodField()

    class Meta:
        model = StudentResults
        fields = [
            'id', 'studentClassName', 'studentClassDescription', 
            'exam_session', 'academic_year', 'board_name', 
            'total_students', 'passed_students', 'pass_rate', 
            'grade_detail', 'certificate_status', 'helpline',
            'resultCreatedAt', 'resultUpdatedAt', 'images', 'latest_update'
        ]

    def get_latest_update(self, obj):
        if obj.images.exists():
            return obj.images.latest('resultSheetUpdatedAt').resultSheetUpdatedAt
        return None

class TopAchieverSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = TopAchiever
        fields = [
            'id',
            'name',
            'image',
            'class_name',
            'achievement_title',
            'board_name',
            'category',
            'category_display',
            'roll_number',
            'academic_year',
            'score_or_division',
            'father_name',
            'address',
            'quote',
            'is_featured',
            'order',
            'created_at',
            'updated_at',
        ]
