from django import forms
from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from server.admin_utils import SupabaseUploadAdminMixin, validate_image_size
from .models import ExpatriateGrant


class ExpatriateGrantAdminForm(forms.ModelForm):
    upload_image = forms.FileField(
        required=False,
        validators=[validate_image_size],
        label="সদস্যের ছবি আপলোড করুন (Supabase Storage)",
        help_text="কম্পিউটার বা মোবাইল থেকে ছবি সিলেক্ট করুন (সর্বোচ্চ ২ MB)। এটি স্বয়ংক্রিয়ভাবে Supabase-এর 'Expatriate donors' বাকেটে আপলোড হবে।"
    )

    class Meta:
        model = ExpatriateGrant
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "image" in self.fields:
            self.fields["image"].required = False
            self.fields["image"].label = "ছবির সরাসরি URL (ঐচ্ছিক)"
            self.fields["image"].help_text = "উপরে ছবি আপলোড করলে এই ফিল্ড স্বয়ংক্রিয়ভাবে পূর্ণ হবে। অথবা সরাসরি ক্লাউড লিঙ্ক দিতে পারেন।"


@admin.register(ExpatriateGrant)
class ExpatriateGrantAdmin(SupabaseUploadAdminMixin, ModelAdmin):
    form = ExpatriateGrantAdminForm
    supabase_upload_field = "upload_image"
    supabase_target_field = "image"
    supabase_folder = "donors"
    supabase_bucket = "Expatriate donors"

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
        "current_image_preview",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Personal Information", {
            "fields": (
                "upload_image",
                "current_image_preview",
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
