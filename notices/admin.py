from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Notice


@admin.register(Notice)
class NoticeAdmin(ModelAdmin):
    list_display = (
        "id",
        "title",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
    )

    list_filter = (
        "created_at",
    )

    ordering = ("-created_at",)

    list_per_page = 20

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Notice Information", {
            "fields": (
                "title",
                "description",
            )
        }),

        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )