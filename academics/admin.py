from django.contrib import admin
# pyrefly: ignore [missing-import]
from unfold.admin import ModelAdmin
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

@admin.register(Academic)
class AcademicAdmin(ModelAdmin):
    list_display = (
        "class_name",
        "category",
        "admission_status",
        "student_count",
        "number_seat",
        "academic_year",
        "class_created",
    )
    list_editable = ("admission_status", "student_count", "number_seat")
    search_fields = ("class_name", "class_title", "category")
    list_filter = ("category", "admission_status", "academic_year")
    ordering = ("class_name",)
    list_per_page = 25


@admin.register(BoardingRule)
class BoardingRuleAdmin(ModelAdmin):
    list_display = ("rule_number", "rule_text_short", "category_label", "importance", "is_active")
    list_editable = ("importance", "is_active")
    list_filter = ("category", "importance", "is_active")
    search_fields = ("rule_text", "category_label")
    ordering = ("rule_number",)
    list_per_page = 30

    def rule_text_short(self, obj):
        return obj.rule_text[:70] + "..." if len(obj.rule_text) > 70 else obj.rule_text
    rule_text_short.short_description = "নীতিমালা"


@admin.register(Holiday)
class HolidayAdmin(ModelAdmin):
    list_display = ("order", "title", "category", "date_range", "duration", "reopen_date", "is_active")
    list_editable = ("duration", "is_active")
    list_filter = ("academic_year", "category", "is_active")
    search_fields = ("title", "date_range", "hijri_date")
    ordering = ("order",)
    list_per_page = 25


@admin.register(ExamSession)
class ExamSessionAdmin(ModelAdmin):
    list_display = ("order", "name", "session_id", "badge", "is_active")
    list_editable = ("badge", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "session_id")
    ordering = ("order",)
    list_per_page = 20


@admin.register(ExamRoutine)
class ExamRoutineAdmin(ModelAdmin):
    list_display = (
        "jamat_name",
        "subject",
        "session_name",
        "date_str",
        "day_name",
        "hall_name",
        "marks",
        "order",
        "is_active",
    )
    list_editable = ("order", "marks", "is_active")
    list_filter = ("session_id", "jamat_id", "is_active")
    search_fields = ("subject", "jamat_name", "date_str", "hall_name")
    ordering = ("session_id", "jamat_id", "order")
    list_per_page = 30


@admin.register(ExamInstruction)
class ExamInstructionAdmin(ModelAdmin):
    list_display = ("order", "instruction_short", "is_active")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("instruction",)
    ordering = ("order",)
    list_per_page = 20

    def instruction_short(self, obj):
        return obj.instruction[:80] + "..." if len(obj.instruction) > 80 else obj.instruction
    instruction_short.short_description = "পরীক্ষার্থীদের বিশেষ নির্দেশনা"


@admin.register(ClassDepartment)
class ClassDepartmentAdmin(ModelAdmin):
    list_display = ("order", "name", "dept_id", "desc", "is_active")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("name", "dept_id")
    ordering = ("order",)
    list_per_page = 20


@admin.register(ClassRoutine)
class ClassRoutineAdmin(ModelAdmin):
    list_display = (
        "jamat_name",
        "period",
        "subject",
        "time_slot",
        "department_name",
        "teacher",
        "room",
        "order",
        "is_active",
    )
    list_editable = ("order", "is_active")
    list_filter = ("department", "jamat_id", "is_active")
    search_fields = ("subject", "teacher", "jamat_name", "room")
    ordering = ("department", "jamat_id", "order")
    list_per_page = 30


@admin.register(DailySchedule)
class DailyScheduleAdmin(ModelAdmin):
    list_display = ("order", "time_slot", "title", "badge", "is_active")
    list_editable = ("badge", "is_active")
    list_filter = ("badge", "is_active")
    search_fields = ("title", "description", "time_slot")
    ordering = ("order",)
    list_per_page = 25


@admin.register(CoCurricularActivity)
class CoCurricularActivityAdmin(ModelAdmin):
    list_display = ("order", "title", "category_label", "timing", "venue", "mentor", "is_active")
    list_editable = ("is_active",)
    list_filter = ("category", "is_active")
    search_fields = ("title", "short_desc", "mentor", "venue")
    ordering = ("order",)
    list_per_page = 20


@admin.register(BoardingMealMenu)
class BoardingMealMenuAdmin(ModelAdmin):
    list_display = ("order", "day_name", "breakfast", "lunch", "dinner", "is_active")
    list_editable = ("breakfast", "lunch", "dinner", "is_active")
    search_fields = ("day_name", "breakfast", "lunch", "dinner")
    ordering = ("order",)
    list_per_page = 10


@admin.register(BoardingMealTiming)
class BoardingMealTimingAdmin(ModelAdmin):
    list_display = ("order", "meal_type", "time_slot", "is_active")
    list_editable = ("time_slot", "is_active")
    ordering = ("order",)


@admin.register(BoardingMealRule)
class BoardingMealRuleAdmin(ModelAdmin):
    list_display = ("order", "rule_text_short", "is_active")
    list_editable = ("is_active",)
    ordering = ("order",)

    def rule_text_short(self, obj):
        return obj.rule_text[:70] + "..." if len(obj.rule_text) > 70 else obj.rule_text
    rule_text_short.short_description = "নীতিমালা"
