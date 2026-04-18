from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Admission


@admin.register(Admission)
class AdmissionAdmin(ModelAdmin):
    list_display = (
        "id",
        "ClassName",
        "class_level",
        "seat_availability",
        "monthly_fee",
        "admission_start_date",
        "admission_end_date",
        "admission_created",
    )

    search_fields = (
        "ClassName",
        "class_level",
    )

    list_filter = (
        "class_level",
        "seat_availability",
        "admission_start_date",
    )

    ordering = ("-admission_created",)

    list_per_page = 20

    readonly_fields = (
        "admission_created",
        "admission_updated",
    )

    fieldsets = (
        ("Basic Information", {
            "fields": (
                "ClassName",
                "class_level",
                "seat_availability",
            )
        }),

        ("Fees Structure", {
            "fields": (
                "form_fee",
                "new_admission_fee",
                "old_admission_fee",
                "new_total_fee",
                "old_total_fee",
                "additional_fee",
                "monthly_fee",
            )
        }),

        ("Admission Timeline", {
            "fields": (
                "admission_start_date",
                "admission_end_date",
            )
        }),

        ("Requirements", {
            "fields": (
                "required_documents",
            )
        }),

        ("Timestamps", {
            "fields": (
                "admission_created",
                "admission_updated",
            )
        }),
    )