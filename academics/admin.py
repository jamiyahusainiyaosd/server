from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Academic


@admin.register(Academic)
class AcademicAdmin(ModelAdmin):
    list_display = (
        "id",
        "class_name",
        "class_title",
        "student_count",
        "number_seat",
        "class_created",
    )

    search_fields = (
        "class_name",
        "class_title",
    )

    list_filter = (
        "class_created",
    )

    ordering = ("-class_created",)

    list_per_page = 20

    readonly_fields = (
        "class_created",
        "class_update",
    )

    fieldsets = (
        ("Basic Information", {
            "fields": (
                "class_name",
                "class_title",
                "class_description",
            )
        }),
        ("Capacity", {
            "fields": (
                "student_count",
                "number_seat",
            )
        }),
        ("Timestamps", {
            "fields": (
                "class_created",
                "class_update",
            )
        }),
    )