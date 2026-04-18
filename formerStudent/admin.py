from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from .models import FormerStudent


@admin.register(FormerStudent)
class FormerStudentAdmin(ModelAdmin):
    list_display = (
        "id",
        "image_preview",
        "name",
        "mobile",
        "address",
        "pass_year",
        "created_at",
    )

    search_fields = (
        "name",
        "mobile",
        "address",
        "current",
    )

    list_filter = (
        "pass_year",
        "created_at",
    )

    ordering = ("-created_at",)

    list_per_page = 20

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Student Information", {
            "fields": (
                "image",
                "name",
                "mobile",
                "address",
                "current",
                "pass_year",
            )
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    def image_preview(self, obj):
        if not obj.image:
            return "-"

        try:
            image_url = obj.image.url
        except AttributeError:
            image_url = obj.image

        return format_html(
            '<img src="{}" width="50" height="50" style="border-radius:6px; object-fit:cover;" />',
            image_url
        )

    image_preview.short_description = "Image"