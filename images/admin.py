from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from .models import Images


def get_image_url(image_field):
    if not image_field:
        return None
    try:
        return image_field.url
    except AttributeError:
        return image_field


@admin.register(Images)
class ImageAdmin(ModelAdmin):
    list_display = (
        "id",
        "image_preview",
    )

    ordering = ("-id",)

    list_per_page = 20

    fieldsets = (
        ("Image Information", {
            "fields": (
                "img",
            )
        }),
    )

    def image_preview(self, obj):
        image_url = get_image_url(obj.img)
        if not image_url:
            return "-"
        return format_html(
            '<img src="{}" width="70" height="70" style="border-radius:6px; object-fit:cover;" />',
            image_url
        )

    image_preview.short_description = "Preview"