from django.db import models
from django.core.exceptions import ValidationError

BENGALI_DIGITS = {'0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪', '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯'}
def to_bn(num):
    return ''.join(BENGALI_DIGITS.get(ch, ch) for ch in str(num))

PRESET_THEME_COLORS = [
    ("#f1f3ff", "অপশন ১: সফট ল্যাভেন্ডার স্লেট (#f1f3ff - মূল ডিফল্ট)"),
    ("#f0f9ff", "অপশন ২: আইস স্কাই ব্লু (#f0f9ff - ফ্রেশ ও ক্রিস্প)"),
    ("#f0fdf4", "অপশন ৩: সফট এমারেল্ড মিন্ট (#f0fdf4 - ইসলামিক ও শান্ত)"),
    ("#f8fafc", "অপশন ৪: ক্ল্যাসিক কর্পোরেট স্লেট (#f8fafc - নিউট্রাল)"),
    ("#fafaf9", "অপশন ৫: ওয়ার্ম ক্রিম পেপার (#fafaf9 - সোবার ওয়ার্ম)"),
    ("#f5f3ff", "অপশন ৬: রয়েল ইন্ডিগো টিন্ট (#f5f3ff - আধুনিক রয়্যাল)"),
    ("#fff7ed", "অপশন ৭: গোল্ডেন সেণ্ড টিন্ট (#fff7ed - ট্র্যাডিশনাল ওয়ার্ম)"),
    ("#f7fee7", "অপশন ৮: সেজ লাইম গ্রিন (#f7fee7 - ন্যাচারাল প্রশান্তি)"),
    ("#fdf4ff", "অপশন ৯: ভায়োলেট রয়্যালটি (#fdf4ff - পেস্টেল ভায়োলেট)"),
    ("#ecfdf5", "অপশন ১০: ডিপ মিন্ট টিন্ট (#ecfdf5 - রিফ্রেশিং গ্রিন)"),
    ("#f1f5f9", "অপশন ১১: কুল গ্লাস স্লেট (#f1f5f9 - মেটালিক স্লেট)"),
    ("#fdf8f6", "অপশন ১২: রোজ কোয়ার্টজ নিউট্রাল (#fdf8f6 - ওয়ার্ম পেস্টেল)"),
    ("#f0fdfa", "অপশন ১৩: সফট টিল মিস্ট (#f0fdfa - ব্লুইশ-গ্রিন মিস্ট)"),
    ("#fff1f2", "অপশন ১৪: ব্লাশ রোজ ক্লাউড (#fff1f2 - লাক্সারি পেস্টেল পিংক)"),
    ("#fffbeb", "অপশন ১৫: ওয়ার্ম ভ্যানিলা গ্লো (#fffbeb - সাটিন গোল্ডেন)"),
    ("#f3f4f6", "অপশন ১৬: মিনিমাল প্ল্যাটিনাম (#f3f4f6 - মিনিমালিস্ট প্ল্যাটিনাম)"),
    ("#eef2ff", "অপশন ১৭: ডিপ হরাইজন ব্লু (#eef2ff - কর্পোরেট ডিপ ব্লু)"),
    ("#fdf2f8", "অপশন ১৮: সফট অরকিড সিল্ক (#fdf2f8 - অভিজাত পার্পল সিল্ক)"),
    ("#fcf4ec", "অপশন ১৯: ওয়ার্ম স্যান্ডালউড (#fcf4ec - রাজকীয় চন্দন টিন্ট)"),
    ("#e0f2fe", "অপশন ২০: সাইয়ান মিন্ট আইস (#e0f2fe - ক্রিস্টাল আইস ক্লিন)"),
]

class ThemeSetting(models.Model):
    bg_alt_color = models.CharField(
        max_length=60,
        default="#f1f3ff",
        verbose_name="সক্রিয় ব্যাকগ্রাউন্ড কালার",
        help_text="তালিকায় থাকা যেকোনো কালার সিলেক্ট করুন।"
    )
    saved_custom_colors = models.JSONField(
        default=list,
        blank=True,
        verbose_name="সংরক্ষিত কাস্টম কালারসমূহ"
    )
    new_custom_color = models.CharField(
        max_length=60,
        blank=True,
        default="",
        verbose_name="নতুন কাস্টম কালার কোড বা নাম লিখুন",
        help_text="নতুন কাস্টম কালার যোগ করতে চাইলে এখানে Hex (#dbeafe), RGB, RGBA বা কালারের নাম লিখুন।"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="সর্বশেষ পরিবর্তনের সময়")

    class Meta:
        verbose_name = "থিম সেটিংস (Theme Setting)"
        verbose_name_plural = "থিম সেটিংস (Theme Settings)"

    def __str__(self):
        return f"ওয়েবসাইট থিম কালার: {self.bg_alt_color}"

    def get_all_choices(self):
        choices = list(PRESET_THEME_COLORS)
        custom_list = self.saved_custom_colors or []
        for idx, col in enumerate(custom_list):
            opt_num = to_bn(21 + idx)
            choices.append((col, f"অপশন {opt_num}: কাস্টম কালার ({col})"))
            
        next_num = to_bn(21 + len(custom_list))
        choices.append(("add_new", f"অপশন {next_num}: নতুন কাস্টম কালার যোগ করুন (নিজের পছন্দমতো কোড বা নাম)"))
        return choices

    def clean(self):
        super().clean()
        new_val = self.new_custom_color.strip() if self.new_custom_color else ""
        if self.bg_alt_color == "add_new" and not new_val:
            raise ValidationError({
                "new_custom_color": "নতুন কাস্টম কালার যোগ করার অপশন সিলেক্ট করলে এই ফিল্ডে কালার কোড বা নাম দেওয়া বাধ্যতামূলক!"
            })

    def save(self, *args, **kwargs):
        if not isinstance(self.saved_custom_colors, list):
            self.saved_custom_colors = []

        new_val = self.new_custom_color.strip() if self.new_custom_color else ""
        if new_val:
            preset_hexes = [p[0].lower() for p in PRESET_THEME_COLORS]
            if new_val not in self.saved_custom_colors and new_val.lower() not in preset_hexes:
                self.saved_custom_colors.append(new_val)
            self.bg_alt_color = new_val
            self.new_custom_color = ""
        elif self.bg_alt_color == "add_new":
            self.bg_alt_color = "#f1f3ff"

        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(
            pk=1,
            defaults={"bg_alt_color": "#F9FAFB", "saved_custom_colors": ["#F9FAFB"]}
        )
        if not obj.saved_custom_colors:
            obj.saved_custom_colors = ["#F9FAFB"]
            obj.bg_alt_color = "#F9FAFB"
            obj.save()
        return obj
