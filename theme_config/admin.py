from django import forms
from django.contrib import admin
from django.shortcuts import redirect
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin
from .models import ThemeSetting, PRESET_THEME_COLORS

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
