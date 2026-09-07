from django import forms
from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from server.admin_utils import SupabaseUploadAdminMixin, validate_image_size
from .models import TeacherModel


class TeacherModelAdminForm(forms.ModelForm):
    upload_image = forms.FileField(
        required=False,
        validators=[validate_image_size],
        label="শিক্ষকের ছবি আপলোড করুন (Supabase Storage)",
        help_text="কম্পিউটার বা ডিভাইস থেকে ছবি নির্বাচন করুন (সর্বোচ্চ ২ MB)। এটি স্বয়ংক্রিয়ভাবে Supabase-এর 'Teachers' বাকেটে আপলোড হবে।"
    )

    class Meta:
        model = TeacherModel
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "image" in self.fields:
            self.fields["image"].required = False
            self.fields["image"].label = "ছবির সরাসরি URL (ঐচ্ছিক)"
            self.fields["image"].help_text = "উপরে ছবি আপলোড করলে এই ফিল্ড স্বয়ংক্রিয়ভাবে পূর্ণ হবে। অথবা সরাসরি ক্লাউড লিঙ্ক দিতে পারেন।"


@admin.register(TeacherModel)
class TeacherModelAdmin(SupabaseUploadAdminMixin, ModelAdmin):
    form = TeacherModelAdminForm
    supabase_upload_field = "upload_image"
    supabase_target_field = "image"
    supabase_folder = "teachers"
    supabase_bucket = "Teachers"

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
        "current_image_preview",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Teacher Information", {
            "fields": (
                "upload_image",
                "current_image_preview",
                "image",
                "name",
                "designation",
                "phone_number",
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
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:6px; object-fit:cover;" />',
                obj.image
            )
        return "-"

    image_preview.short_description = "Image"
