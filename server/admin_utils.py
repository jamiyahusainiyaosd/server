from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from .supabase_storage import upload_file_to_supabase

MAX_IMAGE_SIZE_BYTES = 2 * 1024 * 1024   # 2 MB
MAX_VIDEO_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB


def validate_image_size(file_obj):
    """
    Validates that the uploaded image file is not greater than 2 MB.
    """
    if not file_obj:
        return
    file_size = getattr(file_obj, 'size', None)
    if file_size and file_size > MAX_IMAGE_SIZE_BYTES:
        size_in_mb = round(file_size / (1024 * 1024), 2)
        raise ValidationError(
            f"ছবির সাইজ সর্বোচ্চ ২ MB হতে পারবে। আপনার ফাইলের সাইজ {size_in_mb} MB।"
        )


def validate_video_size(file_obj):
    """
    Validates that the uploaded video file is not greater than 50 MB.
    """
    if not file_obj:
        return
    file_size = getattr(file_obj, 'size', None)
    if file_size and file_size > MAX_VIDEO_SIZE_BYTES:
        size_in_mb = round(file_size / (1024 * 1024), 2)
        raise ValidationError(
            f"ভিডিও ফাইলের সাইজ সর্বোচ্চ ৫০ MB হতে পারবে। আপনার ফাইলের সাইজ {size_in_mb} MB।"
        )


def get_image_url(image_field):
    if not image_field:
        return None
    try:
        return image_field.url
    except AttributeError:
        return str(image_field)


class SupabaseUploadAdminMixin:
    """
    Mixin for ModelAdmin to easily integrate Supabase Storage file uploads.
    """
    supabase_upload_field = "upload_image"
    supabase_target_field = "image"
    supabase_folder = "uploads"
    supabase_bucket = None

    def save_model(self, request, obj, form, change):
        upload_file = form.cleaned_data.get(self.supabase_upload_field)
        if upload_file:
            bucket = getattr(self, 'supabase_bucket', None)
            public_url = upload_file_to_supabase(
                upload_file,
                folder=self.supabase_folder,
                bucket_name=bucket
            )
            setattr(obj, self.supabase_target_field, public_url)
        super().save_model(request, obj, form, change)

    def current_image_preview(self, obj):
        media_url = getattr(obj, self.supabase_target_field, None)
        if not media_url:
            return format_html('<span style="color:#94a3b8; font-size:12px;">কোনো ফাইল নেই</span>')

        url_str = str(media_url).lower()
        is_video = any(ext in url_str for ext in ['.mp4', '.webm', '.ogg', '.mov', 'video%20gallary', 'cloudinary.com'])

        if is_video:
            if '.mp4' in url_str or '.webm' in url_str or 'video%20gallary' in url_str:
                return format_html(
                    '<div style="display:flex; flex-direction:column; gap:6px; margin:4px 0;">'
                    '<video controls src="{}" style="max-height:160px; max-width:280px; border-radius:8px; border:1px solid #cbd5e1; box-shadow:0 2px 4px rgba(0,0,0,0.06);"></video>'
                    '<span style="font-size:11px; color:#64748b;">বর্তমান সংরক্ষিত ভিডিও (Supabase Storage)</span>'
                    '</div>',
                    media_url
                )
            else:
                return format_html(
                    '<div style="display:flex; flex-direction:column; gap:6px; margin:4px 0;">'
                    '<iframe src="{}" style="height:140px; width:250px; border-radius:8px; border:1px solid #cbd5e1;" allowFullScreen></iframe>'
                    '<span style="font-size:11px; color:#64748b;">ভিডিও এম্বেড প্রিভিউ</span>'
                    '</div>',
                    media_url
                )

        return format_html(
            '<div style="display:flex; flex-direction:column; gap:6px; margin:4px 0;">'
            '<img src="{}" style="max-height:160px; max-width:260px; border-radius:8px; object-fit:cover; border:1px solid #cbd5e1; box-shadow:0 2px 4px rgba(0,0,0,0.06);" />'
            '<span style="font-size:11px; color:#64748b;">বর্তমান সংরক্ষিত ছবি (Supabase / Cloud)</span>'
            '</div>',
            media_url
        )

    current_image_preview.short_description = "বর্তমান প্রিভিউ"
