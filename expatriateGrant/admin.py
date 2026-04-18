from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from .models import ExpatriateGrant


@admin.register(ExpatriateGrant)
class ExpatriateGrantAdmin(ModelAdmin):
    list_display = (
        "id",
        "image_preview",
        "name",
        "mobile",
        "member_type",
        "status",
        "chadar_amount",
        "created_at",
    )

    search_fields = (
        "name",
        "mobile",
        "address",
    )

    list_filter = (
        "member_type",
        "status",
        "created_at",
    )

    ordering = ("-created_at",)

    list_per_page = 20

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Personal Information", {
            "fields": (
                "image",
                "name",
                "mobile",
                "address",
            )
        }),
        ("Membership Details", {
            "fields": (
                "member_type",
                "status",
            )
        }),
        ("Financial Information", {
            "fields": (
                "chadar_amount",
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