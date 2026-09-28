import re
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from server.admin_utils import SupabaseUploadAdminMixin, get_image_url, validate_image_size
from server.supabase_storage import upload_file_to_supabase
from .models import StudentResults, StudentResultImage, TopAchiever

CLASS_FOLDER_MAP = {
    'নাজেরা': 'najera',
    'নূরানী শিশু': 'noorani-shishu',
    'নূরানী ১ম': 'noorani-1st-year',
    'নূরানী ২য়': 'noorani-2nd-year',
    'নূরানী ৩য়': 'noorani-3rd-year',
    'ছফ্ফে': 'soffe-huffaz',
    'ইবতেদাইয়্যাহ ৪র্থ': 'ibtedaiyah-4th-year',
    'ইবতেদাইয়্যাহ ৫ম': 'ibtedaiyah-5th-year',
    'মুতাওয়াসসিতাহ ১ম': 'mutawassitah-1st-year',
    'মুতাওয়াসসিতাহ ২য়': 'mutawassitah-2nd-year',
    'মুতাওয়াসসিতাহ ৩য়': 'mutawassitah-3rd-year',
    'সানাবিয়্যাহ আম্মাহ': 'sanabiyyah-ammah',
    'সানাবিয়্যাতুল উলইয়া (উলা)': 'sanabiyyatul-ulya-1st-year',
    'সানাবিয়্যাতুল উলইয়া (ছানিয়া)': 'sanabiyyatul-ulya-2nd-year',
    'ফযিলত ১ম': 'fazilat-1st-year',
    'ফযিলত ২য়': 'fazilat-2nd-year',
}


def get_class_result_folder(class_name):
    if not class_name:
        return "general"
    for key, folder in CLASS_FOLDER_MAP.items():
        if key in class_name:
            return folder
    slug = re.sub(r'[^\w\s-]', '', str(class_name)).strip().lower()
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug or "general"


class StudentResultImageAdminForm(forms.ModelForm):
    upload_image = forms.FileField(
        required=False,
        validators=[validate_image_size],
        label="রেজাল্ট শিট আপলোড করুন (Supabase Storage)",
        help_text="কম্পিউটার বা ডিভাইস থেকে ছবি নির্বাচন করুন (সর্বোচ্চ ২ MB)। এটি স্বয়ংক্রিয়ভাবে ক্লাসের নাম অনুযায়ী Supabase-এর 'Published results' বাকেটে আপলোড হবে।"
    )

    class Meta:
        model = StudentResultImage
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "resultsSheetImg" in self.fields:
            self.fields["resultsSheetImg"].required = False
            self.fields["resultsSheetImg"].label = "রেজাল্ট শিট সরাসরি URL (ঐচ্ছিক)"
            self.fields["resultsSheetImg"].help_text = "উপরে ছবি আপলোড করলে এই ফিল্ড স্বয়ংক্রিয়ভাবে পূর্ণ হবে।"


class StudentResultImageInline(admin.TabularInline):
    model = StudentResultImage
    form = StudentResultImageAdminForm
    extra = 1
    readonly_fields = ("current_preview",)
    fields = ("upload_image", "current_preview", "resultsSheetImg")

    def current_preview(self, obj):
        if obj and obj.resultsSheetImg:
            return format_html(
                '<img src="{}" width="60" height="60" style="border-radius:6px; object-fit:cover;" />',
                obj.resultsSheetImg
            )
        return "-"

    current_preview.short_description = "প্রিভিউ"


@admin.register(StudentResults)
class StudentResultsAdmin(ModelAdmin):
    list_display = (
        "studentClassName",
        "academic_year",
        "total_students",
        "passed_students",
        "pass_rate",
        "resultCreatedAt",
    )

    search_fields = (
        "studentClassName",
        "studentClassDescription",
        "exam_session",
        "board_name",
    )

    list_filter = (
        "academic_year",
        "resultCreatedAt",
    )

    ordering = ("-resultCreatedAt",)
    list_per_page = 20

    readonly_fields = (
        "resultCreatedAt",
        "resultUpdatedAt",
    )

    fieldsets = (
        ("ফলাফলের মূল তথ্য", {
            "fields": (
                "studentClassName",
                "studentClassDescription",
                "exam_session",
                "academic_year",
                "board_name",
            )
        }),
        ("পরীক্ষার্থী ও পাসের পরিসংখ্যান", {
            "fields": (
                "total_students",
                "passed_students",
                "pass_rate",
                "grade_detail",
                "certificate_status",
            )
        }),
        ("Timestamps", {
            "fields": (
                "resultCreatedAt",
                "resultUpdatedAt",
            )
        }),
    )

    inlines = [StudentResultImageInline]

    def save_formset(self, request, form, formset, change):
        class_name = form.instance.studentClassName if form.instance else "general"
        folder = get_class_result_folder(class_name)
        for f in formset.forms:
            if f.cleaned_data.get("upload_image") and f.instance:
                validate_image_size(f.cleaned_data["upload_image"])
                public_url = upload_file_to_supabase(
                    f.cleaned_data["upload_image"],
                    folder=folder,
                    bucket_name="Published results"
                )
                f.instance.resultsSheetImg = public_url
        formset.save()


@admin.register(StudentResultImage)
class StudentResultImageAdmin(SupabaseUploadAdminMixin, ModelAdmin):
    form = StudentResultImageAdminForm
    supabase_upload_field = "upload_image"
    supabase_target_field = "resultsSheetImg"
    supabase_folder = "results"
    supabase_bucket = "Published results"

    list_display = (
        "id",
        "student_result",
        "image_preview",
    )

    search_fields = (
        "student_result__studentClassName",
    )

    ordering = ("-id",)
    list_per_page = 20

    readonly_fields = ("current_image_preview",)

    fieldsets = (
        ("Result Sheet Information", {
            "fields": (
                "student_result",
                "upload_image",
                "current_image_preview",
                "resultsSheetImg",
            )
        }),
    )

    def save_model(self, request, obj, form, change):
        upload_file = form.cleaned_data.get(self.supabase_upload_field)
        if upload_file:
            class_name = obj.student_result.studentClassName if (obj.student_result and obj.student_result.studentClassName) else "general"
            folder = get_class_result_folder(class_name)
            public_url = upload_file_to_supabase(
                upload_file,
                folder=folder,
                bucket_name=self.supabase_bucket
            )
            setattr(obj, self.supabase_target_field, public_url)
        super(ModelAdmin, self).save_model(request, obj, form, change)

    def image_preview(self, obj):
        image_url = get_image_url(obj.resultsSheetImg)
        if not image_url:
            return "-"
        return format_html(
            '<img src="{}" width="70" height="70" style="border-radius:6px; object-fit:cover;" />',
            image_url
        )

    image_preview.short_description = "Preview"


class TopAchieverAdminForm(forms.ModelForm):
    upload_image = forms.FileField(
        required=False,
        validators=[validate_image_size],
        label="কৃতি শিক্ষার্থীর ছবি আপলোড করুন (Supabase Storage)",
        help_text="কম্পিউটার বা ফোন থেকে ছবি নির্বাচন করুন (সর্বোচ্চ ২ MB)। এটি স্বয়ংক্রিয়ভাবে Supabase-এর 'Published results' বাকেটের 'top_achievers' ফোল্ডারে সংরক্ষিত হবে।"
    )

    class Meta:
        model = TopAchiever
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "image" in self.fields:
            self.fields["image"].required = False
            self.fields["image"].label = "ছবির সরাসরি CDN URL (ঐচ্ছিক)"
            self.fields["image"].help_text = "উপরে ছবি আপলোড দিলে এই ফিল্ডটি স্বয়ংক্রিয়ভাবে পূরণ হয়ে যাবে।"


@admin.register(TopAchiever)
class TopAchieverAdmin(SupabaseUploadAdminMixin, ModelAdmin):
    form = TopAchieverAdminForm
    supabase_upload_field = "upload_image"
    supabase_target_field = "image"
    supabase_folder = "top_achievers"
    supabase_bucket = "Published results"

    list_display = (
        "image_preview",
        "name",
        "achievement_title",
        "class_name",
        "category_badge",
        "board_name",
        "academic_year",
        "is_featured",
        "order",
    )

    list_filter = (
        "category",
        "is_featured",
        "academic_year",
        "board_name",
    )

    search_fields = (
        "name",
        "achievement_title",
        "class_name",
        "board_name",
        "roll_number",
        "address",
        "father_name",
    )

    list_editable = ("is_featured", "order")
    ordering = ("order", "-created_at")
    list_per_page = 20

    readonly_fields = ("current_image_preview", "created_at", "updated_at")

    fieldsets = (
        ("শিক্ষার্থী ও অর্জনের তথ্য", {
            "fields": (
                "name",
                "upload_image",
                "current_image_preview",
                "image",
                "achievement_title",
                "category",
                "class_name",
            )
        }),
        ("বোর্ড, পরীক্ষা ও মেধার বিবরণ", {
            "fields": (
                "board_name",
                "academic_year",
                "roll_number",
                "score_or_division",
            )
        }),
        ("ব্যক্তিগত ও বার্তা তথ্য", {
            "fields": (
                "father_name",
                "address",
                "quote",
            )
        }),
        ("প্রদর্শন ও সাজানোর সেটিংস", {
            "fields": (
                "is_featured",
                "order",
                "created_at",
                "updated_at",
            )
        }),
    )

    def image_preview(self, obj):
        image_url = get_image_url(obj.image)
        if not image_url:
            return format_html('<span style="color:#94a3b8; font-size:12px;">ছবি নেই</span>')
        return format_html(
            '<img src="{}" width="48" height="48" style="border-radius:10px; object-fit:cover; border:1px solid #cbd5e1; box-shadow:0 1px 3px rgba(0,0,0,0.08);" />',
            image_url
        )

    image_preview.short_description = "ছবি"

    def category_badge(self, obj):
        colors = {
            'national': '#059669',    # Emerald
            'division': '#2563eb',    # Blue
            'district': '#7c3aed',    # Purple
            'madrasa': '#d97706',     # Amber
        }
        color = colors.get(obj.category, '#475569')
        return format_html(
            '<span style="background-color:{}15; color:{}; border:1px solid {}40; padding:3px 8px; border-radius:9999px; font-weight:600; font-size:11px;">{}</span>',
            color, color, color, obj.get_category_display()
        )

    category_badge.short_description = "অর্জন স্তর"
