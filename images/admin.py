from django import forms
from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from server.admin_utils import SupabaseUploadAdminMixin, get_image_url, validate_image_size
from .models import Images


class ImagesAdminForm(forms.ModelForm):
    upload_image = forms.FileField(
        required=False,
        validators=[validate_image_size],
        label="ছবি আপলোড করুন (Supabase Storage)",
        help_text="কম্পিউটার বা ডিভাইস থেকে সরাসরি ছবি নির্বাচন করুন (সর্বোচ্চ ২ MB)।"
    )

    class Meta:
        model = Images
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "img" in self.fields:
            self.fields["img"].required = False
            self.fields["img"].label = "ছবির সরাসরি URL (ঐচ্ছিক)"
            self.fields["img"].help_text = "উপরে ছবি আপলোড করলে এই ফিল্ড স্বয়ংক্রিয়ভাবে পূর্ণ হবে।"


@admin.register(Images)
class ImageAdmin(SupabaseUploadAdminMixin, ModelAdmin):
    form = ImagesAdminForm
    supabase_upload_field = "upload_image"
    supabase_target_field = "img"
    supabase_folder = "images"

    list_display = (
        "id",
        "image_preview",
    )

    ordering = ("-id",)
    list_per_page = 20

    readonly_fields = ("current_image_preview",)

    fieldsets = (
        ("Image Information", {
            "fields": (
                "upload_image",
                "current_image_preview",
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
