from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from .models import StudentResults, StudentResultImage


def get_image_url(image_field):
    if not image_field:
        return None
    try:
        return image_field.url
    except AttributeError:
        return image_field


class StudentResultImageInline(admin.TabularInline):
    model = StudentResultImage
    extra = 1


@admin.register(StudentResults)
class StudentResultsAdmin(ModelAdmin):
    list_display = (
        "id",
        "studentClassName",
        "studentClassDescription",
        "resultCreatedAt",
    )

    search_fields = (
        "studentClassName",
        "studentClassDescription",
    )

    list_filter = (
        "resultCreatedAt",
    )

    ordering = ("-resultCreatedAt",)

    list_per_page = 20

    readonly_fields = (
        "resultCreatedAt",
        "resultUpdatedAt",
    )

    fieldsets = (
        ("Result Information", {
            "fields": (
                "studentClassName",
                "studentClassDescription",
            )
        }),
        ("Timestamps", {
            "fields": (
                "resultCreatedAt",
                "resultUpdatedAt",
            )
        }),
    )

    inlines = [StudentResultImageInline]


@admin.register(StudentResultImage)
class StudentResultImageAdmin(ModelAdmin):
    list_display = (
        "id",
        "student_result",
        "image_preview",
    )

    search_fields = (
        "student_result__studentClassName",
    )

    ordering = ("-id",)

    list_per_page = 20

    fieldsets = (
        ("Result Sheet Information", {
            "fields": (
                "student_result",
                "resultsSheetImg",
            )
        }),
    )

    def image_preview(self, obj):
        image_url = get_image_url(obj.resultsSheetImg)
        if not image_url:
            return "-"
        return format_html(
            '<img src="{}" width="70" height="70" style="border-radius:6px; object-fit:cover;" />',
            image_url
        )

    image_preview.short_description = "Preview"