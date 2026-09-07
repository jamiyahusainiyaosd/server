from django import forms
from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from server.admin_utils import SupabaseUploadAdminMixin, validate_image_size
from .models import FinanicialReport


class FinanicialReportAdminForm(forms.ModelForm):
    upload_image = forms.FileField(
        required=False,
        validators=[validate_image_size],
        label="আর্থিক রিপোর্ট ছবি আপলোড করুন (Supabase Storage)",
        help_text="কম্পিউটার বা ডিভাইস থেকে রিপোর্ট ছবি সিলেক্ট করুন (সর্বোচ্চ ২ MB)। এটি স্বয়ংক্রিয়ভাবে Supabase-এর 'financialReport' বাকেটে আপলোড হবে।"
    )

    class Meta:
        model = FinanicialReport
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "finanicialReportImage" in self.fields:
            self.fields["finanicialReportImage"].required = False
            self.fields["finanicialReportImage"].label = "রিপোর্ট ছবির সরাসরি URL (ঐচ্ছিক)"
            self.fields["finanicialReportImage"].help_text = "উপরে ছবি আপলোড করলে এই ফিল্ড স্বয়ংক্রিয়ভাবে পূর্ণ হবে। অথবা সরাসরি ক্লাউড লিঙ্ক দিতে পারেন।"

    def clean(self):
        cleaned_data = super().clean()
        upload_image = cleaned_data.get("upload_image")
        report_img = cleaned_data.get("finanicialReportImage")
        if not upload_image and not report_img and not (self.instance and self.instance.finanicialReportImage):
            raise forms.ValidationError("অনুগ্রহ করে একটি রিপোর্ট ছবি আপলোড করুন অথবা ছবির URL দিন।")
        return cleaned_data


@admin.register(FinanicialReport)
class FinanicialReportAdmin(SupabaseUploadAdminMixin, ModelAdmin):
    form = FinanicialReportAdminForm
    supabase_upload_field = "upload_image"
    supabase_target_field = "finanicialReportImage"
    supabase_folder = "reports"
    supabase_bucket = "financialReport"

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
        "current_image_preview",
        "finanicialReportCreate",
        "finanicialReportUpdate",
    )

    fieldsets = (
        ("Report Information", {
            "fields": (
                "finanicialReportName",
                "finanicialReportDescription",
                "upload_image",
                "current_image_preview",
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
