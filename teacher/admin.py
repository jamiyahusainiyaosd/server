from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from .models import TeacherModel


@admin.register(TeacherModel)
class TeacherModelAdmin(ModelAdmin):
    list_display = (
        "id",
        "image_preview",
        "name",
        "designation",
        "phone_number",
        "created_at",
    )

    search_fields = (
        "name",
        "designation",
        "phone_number",
    )

    list_filter = (
        "designation",
        "created_at",
    )

    ordering = ("-created_at",)

    list_per_page = 20

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Teacher Information", {
            "fields": (
                "name",
                "designation",
                "phone_number",
                "image",
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
        if hasattr(obj, "image") and obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:6px; object-fit:cover;" />',
                obj.image.url
            )
        return "-"

    image_preview.short_description = "Image"