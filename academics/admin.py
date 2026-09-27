from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Academic


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

    list_editable = (
        "admission_status",
        "student_count",
        "number_seat",
    )

    search_fields = (
        "class_name",
        "class_title",
        "category",
    )

    list_filter = (
        "category",
        "admission_status",
        "academic_year",
        "class_created",
    )

    ordering = ("class_name",)
    list_per_page = 25

    readonly_fields = (
        "class_created",
        "class_update",
    )

    fieldsets = (
        ("প্রাথমিক তথ্য", {
            "fields": (
                "class_name",
                "class_title",
                "category",
                "course_code",
                "admission_status",
                "academic_year",
                "class_description",
            )
        }),
        ("আসন ও ছাত্র পরিসংখ্যান", {
            "fields": (
                "student_count",
                "number_seat",
            )
        }),
        ("প্রধান বৈশিষ্ট্য ও বিষয়সূচি (৪টি কার্ড)", {
            "fields": (
                "feature_1_title", "feature_1_desc",
                "feature_2_title", "feature_2_desc",
                "feature_3_title", "feature_3_desc",
                "feature_4_title", "feature_4_desc",
            )
        }),
        ("দৈনিক ক্লাস রুটিন ও অধিবেশন (৩টি পর্ব)", {
            "fields": (
                "routine_badge",
                "routine_1_time", "routine_1_title",
                "routine_2_time", "routine_2_title",
                "routine_3_time", "routine_3_title",
            )
        }),
        ("উস্তাদদের তত্ত্বাবধান নোট", {
            "fields": (
                "teacher_note",
            )
        }),
        ("Timestamps", {
            "fields": (
                "class_created",
                "class_update",
            )
        }),
    )
