from django import forms
from django.contrib import admin
from django.shortcuts import redirect
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin
from .models import ThemeSetting, PrayerTime, AdmissionStatus, ContactSetting, PRESET_THEME_COLORS

GRID_STYLE = """
<style>
.theme-color-radio-list {
    display: grid !important;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)) !important;
    gap: 10px !important;
    padding: 0 !important;
    list-style: none !important;
    margin-top: 10px !important;
}
.theme-color-radio-list li {
    background: #ffffff !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    display: flex !important;
    align-items: center !important;
    transition: all 0.15s ease !important;
    cursor: pointer !important;
}
.theme-color-radio-list li:hover {
    border-color: #009B63 !important;
    background-color: #f8fafc !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06) !important;
}
.theme-color-radio-list input[type="radio"] {
    margin-right: 12px !important;
    accent-color: #009B63 !important;
    width: 18px !important;
    height: 18px !important;
    cursor: pointer !important;
}
.theme-color-radio-list label {
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    width: 100% !important;
    margin: 0 !important;
}
</style>
"""

class ThemeSettingAdminForm(forms.ModelForm):
    class Meta:
        model = ThemeSetting
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if not instance:
            instance = ThemeSetting.get_solo()

        all_choices = instance.get_all_choices()
        radio_choices = []
        for val, label in all_choices:
            if val == "add_new":
                swatch_style = "background: linear-gradient(135deg, #f43f5e, #8b5cf6, #06b6d4, #10b981);"
            else:
                swatch_style = f"background-color: {val};"
            
            label_html = mark_safe(
                f'<span style="display:inline-flex; align-items:center; gap:10px; vertical-align:middle;">'
                f'<span style="width:24px; height:24px; border-radius:6px; {swatch_style} border:1px solid #cbd5e1; box-shadow:0 1px 2px rgba(0,0,0,0.06); display:inline-block; flex-shrink:0;"></span>'
                f'<span style="font-weight:600; font-size:13px; color:#1e293b;">{label}</span>'
                f'</span>'
            )
            radio_choices.append((val, label_html))

        self.fields['bg_alt_color'].widget = forms.RadioSelect(
            choices=radio_choices,
            attrs={'class': 'theme-color-radio-list'}
        )
        self.fields['bg_alt_color'].label = mark_safe('যেকোনো একটি কালার সিলেক্ট করুন (সরাসরি ক্লিক করুন):' + GRID_STYLE)
        self.fields['bg_alt_color'].help_text = 'পূর্বে সেভ করা যেকোনো কালার সরাসরি সিলেক্ট করতে পারেন অথবা সবার শেষের অপশনে নতুন কালার যোগ করতে পারেন।'
        
        self.fields['new_custom_color'].label = mark_safe(
            'নতুন কাস্টম কালার কোড বা নাম <span style="color:#ef4444; font-weight:bold; font-size:13px;">* (যদি নতুন কালার যোগ করতে চান)</span>'
        )

    def clean(self):
        cleaned_data = super().clean()
        bg_alt_color = cleaned_data.get('bg_alt_color')
        new_custom_color = cleaned_data.get('new_custom_color')

        if bg_alt_color == 'add_new':
            if not new_custom_color or not new_custom_color.strip():
                self.add_error(
                    'new_custom_color',
                    'নতুন কাস্টম কালার অপশন সিলেক্ট করলে এই ফিল্ডে কালার কোড (যেমন: #f1f5f9) বা নাম দেওয়া বাধ্যতামূলক!'
                )
        return cleaned_data


@admin.register(ThemeSetting)
class ThemeSettingAdmin(ModelAdmin):
    form = ThemeSettingAdminForm
    list_display = ('theme_title', 'color_preview_badge', 'bg_alt_color', 'updated_at')
    readonly_fields = ('color_preview_box', 'updated_at')

    fieldsets = (
        ('ওয়েবসাইট ব্যাকগ্রাউন্ড থিম নির্বাচন', {
            'fields': (
                'color_preview_box',
                'bg_alt_color',
            ),
            'description': '২০টি রেডিমেড কালার এবং আপনার যোগ করা কাস্টম কালারগুলো নিচে সরাসরি প্রদর্শিত রয়েছে। যেকোনোটিতে ক্লিক করে Save দিতে পারবেন।'
        }),
        ('নতুন কাস্টম কালার যোগ করার ইনপুট', {
            'fields': (
                'new_custom_color',
            ),
            'description': 'তালিকায় নতুন কোনো কালার যোগ করতে চাইলে এখানে কোড (যেমন: #dbeafe বা rgb(...)) লিখে Save দিন। সাথে সাথে এটি তালিকায় স্থায়ী অপশন হিসেবে যুক্ত হবে এবং পরবর্তী নতুন স্লট তৈরি হবে।'
        }),
        ('সিস্টেম তথ্য', {
            'fields': ('updated_at',),
            'classes': ('collapse',),
        }),
    )

    def changelist_view(self, request, extra_context=None):
        obj = ThemeSetting.get_solo()
        return redirect(f'/admin/theme_config/themesetting/{obj.id}/change/')

    def theme_title(self, obj):
        return 'ওয়েবসাইট থিম কালার সেটিংস'
    theme_title.short_description = 'সেটিংস'

    def color_preview_badge(self, obj):
        color = obj.bg_alt_color if obj and obj.bg_alt_color else '#f1f3ff'
        return format_html(
            '<div style="display:inline-flex; align-items:center; gap:8px;">'
            '<span style="display:inline-block; width:22px; height:22px; border-radius:6px; background-color:{}; border:1px solid #cbd5e1; box-shadow:0 1px 2px rgba(0,0,0,0.05);"></span>'
            '<code style="font-weight:600; font-size:12px;">{}</code>'
            '</div>',
            color,
            color
        )
    color_preview_badge.short_description = 'বর্তমান সক্রিয় কালার প্রিভিউ'

    def color_preview_box(self, obj):
        color = obj.bg_alt_color if obj and obj.bg_alt_color else '#f1f3ff'
        return format_html(
            '<div style="padding:16px 20px; border-radius:12px; background-color:{}; border:1.5px solid #cbd5e1; max-width:520px; display:flex; align-items:center; gap:16px; margin-bottom:14px; box-shadow:0 1px 3px rgba(0,0,0,0.05);">'
            '<div style="width:74px; height:46px; border-radius:8px; background:#ffffff; border:1px solid #e2e8f0; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:11px; text-align:center; color:#0f172a; box-shadow:0 1px 2px rgba(0,0,0,0.05); line-height:46px; flex-shrink:0;">সাদা কার্ড</div>'
            '<div>'
            '<div style="font-weight:700; color:#0f172a; font-size:14px;">লাইভ প্রিভিউ: সাদা কার্ড ও বর্তমান ব্যাকগ্রাউন্ড</div>'
            '<div style="font-size:12px; color:#475569; margin-top:3px;">বর্তমানে সেভ করা সক্রিয় কালার: <code style="font-weight:bold; background:rgba(0,0,0,0.06); padding:2px 6px; border-radius:4px;">{}</code></div>'
            '</div>'
            '</div>',
            color,
            color
        )
    color_preview_box.short_description = 'বর্তমান সক্রিয় কালার প্রিভিউ'

    def has_add_permission(self, request):
        return not ThemeSetting.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AdmissionStatus)
class AdmissionStatusAdmin(ModelAdmin):
    list_display = ("status_title", "status_badge", "session_name", "updated_at")
    readonly_fields = ("status_badge", "updated_at")

    fieldsets = (
        ("ভর্তি কার্যক্রমের মূল নিয়ন্ত্রণ (১-ক্লিক সুইচ)", {
            "fields": (
                "is_open",
                "status_badge",
                "session_name",
            ),
            "description": "এখান থেকে টিক চিহ্ন দিয়ে বা তুলে ১ ক্লিকে পুরো ওয়েবসাইটে ভর্তি চালু বা বন্ধ করতে পারবেন।"
        }),
        ("ওয়েবসাইট ব্যাজ টেক্সট কাস্টমাইজেশন", {
            "fields": (
                "badge_text_open",
                "badge_text_closed",
            ),
            "description": "হেডার এবং হোমপেজের বাটনের গায়ে প্রদর্শিত লেখার পরিবর্তন।"
        }),
        ("অভিভাবকদের জন্য বার্তা ও নোটিশ", {
            "fields": (
                "notice_title",
                "notice_text",
            ),
            "description": "ভর্তি ফরম পেজে বা হোমপেজে প্রদর্শিত নোটিশ।"
        }),
        ("সিস্টেম তথ্য", {
            "fields": ("updated_at",),
            "classes": ("collapse",),
        }),
    )

    def changelist_view(self, request, extra_context=None):
        obj = AdmissionStatus.get_solo()
        return redirect(f"/admin/theme_config/admissionstatus/{obj.id}/change/")

    def status_title(self, obj):
        return "ভর্তি কার্যক্রম ও সেশন নিয়ন্ত্রণ"
    status_title.short_description = "সেটিংস"

    def status_badge(self, obj):
        if obj.is_open:
            return format_html(
                '<span style="background:#dcfce7; color:#15803d; font-weight:bold; padding:5px 14px; border-radius:9999px; border:1px solid #86efac; display:inline-flex; align-items:center; gap:6px; font-size:12px;">'
                '<span style="width:8px; height:8px; border-radius:50%; background:#22c55e;"></span>'
                'ভর্তি চালু আছে ({})'
                '</span>',
                obj.badge_text_open
            )
        else:
            return format_html(
                '<span style="background:#fee2e2; color:#b91c1c; font-weight:bold; padding:5px 14px; border-radius:9999px; border:1px solid #fca5a5; display:inline-flex; align-items:center; gap:6px; font-size:12px;">'
                '<span style="width:8px; height:8px; border-radius:50%; background:#ef4444;"></span>'
                'ভর্তি বন্ধ ({})'
                '</span>',
                obj.badge_text_closed
            )
    status_badge.short_description = "লাইভ স্ট্যাটাস প্রিভিউ"

    def has_add_permission(self, request):
        return not AdmissionStatus.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PrayerTime)
class PrayerTimeAdmin(ModelAdmin):
    list_display = ("prayer_title", "status_badge", "fajr", "zuhr", "asr", "maghrib", "isha", "jummah", "updated_at")
    readonly_fields = ("status_badge", "updated_at")

    fieldsets = (
        ("নামাজের সময়সূচির প্রদর্শন নিয়ন্ত্রণ", {
            "fields": (
                "is_active",
                "status_badge",
                "title",
                "sub_title",
            ),
            "description": "হোমপেজে নামাজের জামা'আত কার্ড দেখানো বা লুকানোর জন্য 'is_active' সুইচ ব্যবহার করুন।"
        }),
        ("৫ ওয়াক্ত ও জুমু'আ জামা'আতের সময়", {
            "fields": (
                "fajr",
                "zuhr",
                "asr",
                "maghrib",
                "isha",
                "jummah",
            ),
            "description": "প্রতিটি ওয়াক্তের জামা'আতের সময় নির্ধারণ করুন (যেমন: ৫:১৫ AM, ১:৩০ PM)।"
        }),
        ("সাহরী, ইফতার ও অতিরিক্ত নোট", {
            "fields": (
                "sehri_end",
                "iftar",
                "special_note",
            ),
            "description": "রমজান বা নফল রোজার সাহরী-ইফতার এবং জামা'আতের বিশেষ কোনো নির্দেশনা।"
        }),
        ("সিস্টেম তথ্য", {
            "fields": ("updated_at",),
            "classes": ("collapse",),
        }),
    )

    def changelist_view(self, request, extra_context=None):
        obj = PrayerTime.get_solo()
        return redirect(f"/admin/theme_config/prayertime/{obj.id}/change/")

    def prayer_title(self, obj):
        return f"{obj.title} ({obj.sub_title})"
    prayer_title.short_description = "সময়সূচি"

    def status_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background:#dcfce7; color:#15803d; font-weight:bold; padding:4px 12px; border-radius:9999px; border:1px solid #86efac; display:inline-flex; align-items:center; gap:6px; font-size:12px;">'
                '<span style="width:8px; height:8px; border-radius:50%; background:#22c55e;"></span>'
                'হোমপেজে প্রদর্শিত হচ্ছে (Active)'
                '</span>'
            )
        else:
            return format_html(
                '<span style="background:#f1f5f9; color:#64748b; font-weight:bold; padding:4px 12px; border-radius:9999px; border:1px solid #cbd5e1; display:inline-flex; align-items:center; gap:6px; font-size:12px;">'
                '<span style="width:8px; height:8px; border-radius:50%; background:#94a3b8;"></span>'
                'লুকানো রয়েছে (Hidden)'
                '</span>'
            )
    status_badge.short_description = "প্রদর্শন স্ট্যাটাস"

    def has_add_permission(self, request):
        return not PrayerTime.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ContactSetting)
class ContactSettingAdmin(ModelAdmin):
    list_display = ("contact_title", "primary_phone", "whatsapp_number", "primary_email", "bkash_display", "updated_at")
    readonly_fields = ("live_overview", "updated_at")

    fieldsets = (
        ("বর্তমান যোগাযোগ ও পেমেন্ট তথ্য সংক্ষেপ", {
            "fields": ("live_overview",),
            "description": "ওয়েবসাইটে বর্তমানে সক্রিয় ফোন, হোয়াটসঅ্যাপ, ইমেইল এবং মোবাইল ব্যাংকিং প্রিভিউ।"
        }),
        ("ফোন নম্বর ও হোয়াটসঅ্যাপ হেল্পলাইন (Phone & WhatsApp)", {
            "fields": (
                ("primary_phone", "primary_phone_label"),
                ("secondary_phone", "secondary_phone_label"),
                ("whatsapp_number", "whatsapp_label"),
            ),
            "description": "ওয়েবসাইটের হেডার, ফুটার, নোটিশ ও যোগাযোগ পেজে প্রদর্শিত হবে।"
        }),
        ("মোবাইল ব্যাংকিং (বিকাশ, নগদ, রকেট - ফি ও দান সংগ্রহ)", {
            "fields": (
                ("bkash_number", "bkash_type"),
                ("nagad_number", "nagad_type"),
                ("rocket_number", "rocket_type"),
            ),
            "description": "শিক্ষার্থীদের ফি ও শুভাকাঙ্ক্ষীদের দান সংগ্রহের নম্বর ও অ্যাকাউন্ট টাইপ।"
        }),
        ("অফিসিয়াল ইমেইল ঠিকানা (Email Addresses)", {
            "fields": (
                ("primary_email", "primary_email_label"),
                ("secondary_email", "secondary_email_label"),
            ),
            "description": "মাদরাসার প্রধান ইমেইল ও বিকল্প/ভর্তি সংক্রান্ত ইমেইল ঠিকানা।"
        }),
        ("মাদরাসার ঠিকানা, গুগল ম্যাপ ও অফিস সময়", {
            "fields": (
                "address",
                "office_hours",
                "google_maps_url",
            ),
            "description": "দর্শনার্থী ও অভিভাবকদের জন্য উন্মুক্ত অফিস সময় ও লোকেশন।"
        }),
        ("সোশ্যাল মিডিয়া পেজ লিংক (Social Media)", {
            "fields": (
                ("facebook_url", "youtube_url"),
            ),
            "classes": ("collapse",),
        }),
        ("সিস্টেম তথ্য", {
            "fields": ("updated_at",),
            "classes": ("collapse",),
        }),
    )

    def changelist_view(self, request, extra_context=None):
        obj = ContactSetting.get_solo()
        return redirect(f"/admin/theme_config/contactsetting/{obj.id}/change/")

    def contact_title(self, obj):
        return "যোগাযোগ ও হেল্পলাইন তথ্য"
    contact_title.short_description = "সেটিংস"

    def bkash_display(self, obj):
        if obj.bkash_number:
            return f"বিকাশ: {obj.bkash_number} ({obj.get_bkash_type_display()})"
        return "সেট করা নেই"
    bkash_display.short_description = "মোবাইল ব্যাংকিং"

    def live_overview(self, obj):
        phone_badge = f'<span style="background:#e0f2fe; color:#0369a1; padding:3px 8px; border-radius:6px; font-weight:600; font-family:monospace;">{obj.primary_phone}</span>'
        whatsapp_badge = f'<span style="background:#dcfce7; color:#15803d; padding:3px 8px; border-radius:6px; font-weight:600; font-family:monospace;">{obj.whatsapp_number or "নেই"}</span>'
        email_badge = f'<span style="background:#f1f5f9; color:#334155; padding:3px 8px; border-radius:6px; font-weight:600;">{obj.primary_email}</span>'
        bkash_badge = f'<span style="background:#fce7f3; color:#be185d; padding:3px 8px; border-radius:6px; font-weight:600; font-family:monospace;">{obj.bkash_number or "নেই"} ({obj.get_bkash_type_display()})</span>'
        nagad_badge = f'<span style="background:#ffedd5; color:#c2410c; padding:3px 8px; border-radius:6px; font-weight:600; font-family:monospace;">{obj.nagad_number or "নেই"}</span>'

        return format_html(
            '<div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:10px; padding:14px; display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:12px; font-size:13px;">'
            '<div><span style="color:#64748b; font-size:11px; display:block; margin-bottom:2px;">📞 প্রধান ফোন:</span>{}</div>'
            '<div><span style="color:#64748b; font-size:11px; display:block; margin-bottom:2px;">💬 হোয়াটসঅ্যাপ:</span>{}</div>'
            '<div><span style="color:#64748b; font-size:11px; display:block; margin-bottom:2px;">✉️ প্রধান ইমেইল:</span>{}</div>'
            '<div><span style="color:#64748b; font-size:11px; display:block; margin-bottom:2px;">🌸 বিকাশ:</span>{}</div>'
            '<div><span style="color:#64748b; font-size:11px; display:block; margin-bottom:2px;">🔶 নগদ:</span>{}</div>'
            '</div>',
            format_html(phone_badge),
            format_html(whatsapp_badge),
            format_html(email_badge),
            format_html(bkash_badge),
            format_html(nagad_badge)
        )
    live_overview.short_description = "লাইভ প্রিভিউ"

    def has_add_permission(self, request):
        return not ContactSetting.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
