from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from .models import PhotoGallary, VideoGallary


def get_image_url(image_field):
    if not image_field:
        return None
    try:
        return image_field.url
    except AttributeError:
        return image_field


@admin.register(PhotoGallary)
class PhotoGallaryAdmin(ModelAdmin):
    list_display = (
        "id",
        "photo_preview",
        "photoTitle",
    )

    search_fields = (
        "photoTitle",
    )

    ordering = ("-id",)

    list_per_page = 20

    fieldsets = (
        ("Photo Information", {
            "fields": (
                "photoTitle",
                "photoImg",
            )
        }),
    )

    def photo_preview(self, obj):
        image_url = get_image_url(obj.photoImg)
        if not image_url:
            return "-"
        return format_html(
            '<img src="{}" width="60" height="60" style="border-radius:6px; object-fit:cover;" />',
            image_url
        )

    photo_preview.short_description = "Preview"


@admin.register(VideoGallary)
class VideoGallaryAdmin(ModelAdmin):
    list_display = (
        "id",
        "video_preview",
        "videoTitle",
    )

    search_fields = (
        "videoTitle",
    )

    ordering = ("-id",)

    list_per_page = 20

    fieldsets = (
        ("Video Information", {
            "fields": (
                "videoTitle",
                "videoImg",
            )
        }),
    )

    def video_preview(self, obj):
        image_url = get_image_url(obj.videoImg)
        if not image_url:
            return "-"
        return format_html(
            '<img src="{}" width="60" height="60" style="border-radius:6px; object-fit:cover;" />',
            image_url
        )

    video_preview.short_description = "Thumbnail"