from rest_framework import serializers
from .models import Academic

class AcademicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Academic
        fields = [
            'id', 'class_name', 'class_title', 'class_description',
            'category', 'course_code', 'admission_status', 'academic_year',
            'routine_badge', 'teacher_note',
            'student_count', 'number_seat',
            'feature_1_title', 'feature_1_desc',
            'feature_2_title', 'feature_2_desc',
            'feature_3_title', 'feature_3_desc',
            'feature_4_title', 'feature_4_desc',
            'routine_1_time', 'routine_1_title',
            'routine_2_time', 'routine_2_title',
            'routine_3_time', 'routine_3_title',
            'class_created', 'class_update'
        ]
