from django import forms
from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from server.admin_utils import SupabaseUploadAdminMixin, get_image_url, validate_image_size, validate_video_size
from .models import PhotoGallary, VideoGallary


class PhotoGallaryAdminForm(forms.ModelForm):
    upload_photo = forms.FileField(
        required=False,
        validators=[validate_image_size],
        label="সরাসরি ছবি আপলোড করুন (Supabase Storage)",
        help_text="কম্পিউটার বা মোবাইল থেকে ছবি সিলেক্ট করুন (সর্বোচ্চ ২ MB)। এটি স্বয়ংক্রিয়ভাবে 'photos' ফোল্ডারে আপলোড হয়ে যাবে।"
    )

    class Meta:
        model = PhotoGallary
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "photoImg" in self.fields:
            self.fields["photoImg"].required = False
            self.fields["photoImg"].label = "ছবির সরাসরি URL (ঐচ্ছিক)"
            self.fields["photoImg"].help_text = "উপরে ফাইল আপলোড করলে এই ফিল্ড স্বয়ংক্রিয়ভাবে পূর্ণ হবে। অথবা সরাসরি ক্লাউড লিংক দিতে পারেন।"

    def clean(self):
        cleaned_data = super().clean()
        upload_photo = cleaned_data.get("upload_photo")
        photo_img = cleaned_data.get("photoImg")
        if not upload_photo and not photo_img and not (self.instance and self.instance.photoImg):
            raise forms.ValidationError("অনুগ্রহ করে একটি ছবি আপলোড করুন অথবা ছবির URL দিন।")
        return cleaned_data


@admin.register(PhotoGallary)
class PhotoGallaryAdmin(SupabaseUploadAdminMixin, ModelAdmin):
    form = PhotoGallaryAdminForm
    supabase_upload_field = "upload_photo"
    supabase_target_field = "photoImg"
    supabase_folder = "photos"
    supabase_bucket = "Photo Gallary"

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

    readonly_fields = ("current_image_preview",)

    fieldsets = (
        ("ফটো গ্যালারি তথ্য", {
            "fields": (
                "photoTitle",
                "upload_photo",
                "current_image_preview",
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


class VideoGallaryAdminForm(forms.ModelForm):
    upload_video = forms.FileField(
        required=False,
        validators=[validate_video_size],
        label="সরাসরি ভিডিও ফাইল আপলোড করুন (Supabase Storage)",
        help_text="কম্পিউটার বা ডিভাইস থেকে ভিডিও ফাইল (.mp4, .webm ইত্যাদি, সর্বোচ্চ ৫০ MB) নির্বাচন করুন। এটি স্বয়ংক্রিয়ভাবে Supabase-এর 'Video Gallary' বাকেটে আপলোড হবে।"
    )

    class Meta:
        model = VideoGallary
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "videoImg" in self.fields:
            self.fields["videoImg"].required = False
            self.fields["videoImg"].label = "অথবা ভিডিও / ইউটিউব / ক্লাউড URL (ঐচ্ছিক)"
            self.fields["videoImg"].help_text = "উপরে ভিডিও ফাইল আপলোড করলে এটি স্বয়ংক্রিয়ভাবে পূর্ণ হবে। অথবা সরাসরি ইউটিউব বা ভিডিও লিঙ্ক দিতে পারেন।"

    def clean(self):
        cleaned_data = super().clean()
        upload_video = cleaned_data.get("upload_video")
        video_img = cleaned_data.get("videoImg")
        if not upload_video and not video_img and not (self.instance and self.instance.videoImg):
            raise forms.ValidationError("অনুগ্রহ করে একটি ভিডিও আপলোড করুন অথবা ভিডিওর URL দিন।")
        return cleaned_data


@admin.register(VideoGallary)
class VideoGallaryAdmin(SupabaseUploadAdminMixin, ModelAdmin):
    form = VideoGallaryAdminForm
    supabase_upload_field = "upload_video"
    supabase_target_field = "videoImg"
    supabase_folder = "videos"
    supabase_bucket = "Video Gallary"

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

    readonly_fields = ("current_image_preview",)

    fieldsets = (
        ("ভিডিও গ্যালারি তথ্য", {
            "fields": (
                "videoTitle",
                "upload_video",
                "current_image_preview",
                "videoImg",
            )
        }),
    )

    def video_preview(self, obj):
        image_url = get_image_url(obj.videoImg)
        if not image_url:
            return "-"
        url_str = str(image_url).lower()
        if '.mp4' in url_str or '.webm' in url_str or 'video%20gallary' in url_str:
            return format_html(
                '<video src="{}" style="width:80px; height:50px; border-radius:6px; object-fit:cover; background:#0f172a;"></video>',
                image_url
            )
        return format_html(
            '<div style="width:80px; height:50px; border-radius:6px; background:#0f172a; display:flex; align-items:center; justify-content:center; color:#34d399; font-size:10px; font-weight:600; text-align:center; padding:2px;">ভিডিও লিংক</div>'
        )

    video_preview.short_description = "Preview"
