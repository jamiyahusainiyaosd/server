from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from .models import FinanicialReport


@admin.register(FinanicialReport)
class FinanicialReportAdmin(ModelAdmin):
    list_display = (
        "id",
        "finanicialReportName",
        "image_preview",
        "finanicialReportCreate",
    )

    search_fields = (
        "finanicialReportName",
        "finanicialReportDescription",
    )

    list_filter = (
        "finanicialReportCreate",
    )

    ordering = ("-finanicialReportCreate",)

    list_per_page = 20

    readonly_fields = (
        "finanicialReportCreate",
        "finanicialReportUpdate",
    )

    fieldsets = (
        ("Report Information", {
            "fields": (
                "finanicialReportName",
                "finanicialReportDescription",
                "finanicialReportImage",
            )
        }),
        ("Timestamps", {
            "fields": (
                "finanicialReportCreate",
                "finanicialReportUpdate",
            )
        }),
    )

    def image_preview(self, obj):
        if obj.finanicialReportImage:
            return format_html(
                '<img src="{}" width="60" height="60" style="border-radius:6px; object-fit:cover;" />',
                obj.finanicialReportImage
            )
        return "-"

    image_preview.short_description = "Preview"