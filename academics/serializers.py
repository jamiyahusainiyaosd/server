import json
from rest_framework import serializers
from .models import (
    Academic,
    BoardingRule,
    Holiday,
    ExamSession,
    ExamRoutine,
    ExamInstruction,
    ClassDepartment,
    ClassRoutine,
    DailySchedule,
    CoCurricularActivity,
    BoardingMealMenu,
    BoardingMealTiming,
    BoardingMealRule,
)

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

class BoardingRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardingRule
        fields = '__all__'

class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = '__all__'

class ExamSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamSession
        fields = '__all__'

class ExamRoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamRoutine
        fields = '__all__'

class ExamInstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamInstruction
        fields = '__all__'

class ClassDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassDepartment
        fields = '__all__'

class ClassRoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoutine
        fields = '__all__'

class DailyScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailySchedule
        fields = '__all__'

class CoCurricularActivitySerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = CoCurricularActivity
        fields = [
            'id', 'activity_id', 'title', 'short_desc', 'full_desc',
            'category', 'category_label', 'timing', 'venue', 'mentor',
            'badge', 'icon', 'items_json', 'items', 'order', 'is_active',
            'created_at', 'updated_at'
        ]

    def get_items(self, obj):
        if not obj.items_json:
            return []
        try:
            return json.loads(obj.items_json)
        except Exception:
            return [line.strip() for line in obj.items_json.split('\n') if line.strip()]


class BoardingMealMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardingMealMenu
        fields = '__all__'


class BoardingMealTimingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardingMealTiming
        fields = '__all__'


class BoardingMealRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardingMealRule
        fields = '__all__'
