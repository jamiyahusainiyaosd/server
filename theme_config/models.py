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
        verbose_name = "১. থিম সেটিংস (Theme Settings)"
        verbose_name_plural = "১. থিম সেটিংস (Theme Settings)"

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


class AdmissionStatus(models.Model):
    is_open = models.BooleanField(
        default=True,
        verbose_name="ভর্তি কার্যক্রম চালু আছে?",
        help_text="টিক চিহ্ন দেওয়া থাকলে পুরো ওয়েবসাইটে 'ভর্তি চলছে' সবুজ ব্যাজ থাকবে এবং আবেদন ফরম সচল থাকবে।"
    )
    badge_text_open = models.CharField(
        max_length=50,
        default="চলমান",
        verbose_name="চালু অবস্থার ব্যাজ টেক্সট",
        help_text="যেমন: চলমান, ভর্তি চলছে"
    )
    badge_text_closed = models.CharField(
        max_length=50,
        default="ভর্তি সমাপ্ত",
        verbose_name="বন্ধ অবস্থার ব্যাজ টেক্সট",
        help_text="যেমন: ভর্তি সমাপ্ত, শীঘ্রই শুরু"
    )
    session_name = models.CharField(
        max_length=100,
        default="শিক্ষাবর্ষ: ২০২৬-২০২৭",
        verbose_name="বর্তমান শিক্ষাবর্ষ",
        help_text="যেমন: শিক্ষাবর্ষ: ২০২৬-২০২৭"
    )
    notice_title = models.CharField(
        max_length=255,
        default="ভর্তি সংক্রান্ত জরুরি নোটিশ",
        verbose_name="নোটিশের শিরোনাম"
    )
    notice_text = models.TextField(
        default="অত্র মাদরাসায় সকল বিভাগে সীমিত আসনে নতুন ছাত্র ভর্তি কার্যক্রম চলছে। আগ্রহী অভিভাবকগণ দ্রুত অনলাইনে আবেদন করুন বা মাদরাসা অফিসে যোগাযোগ করুন।",
        verbose_name="ভর্তি সংক্রান্ত বার্তা / বন্ধকালীন নোটিশ",
        help_text="ভর্তি চালু বা বন্ধ থাকলে যে বিশেষ বার্তাটি অভিভাবকদের প্রদর্শিত হবে।"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="সর্বশেষ আপডেট")

    class Meta:
        verbose_name = "২. ভর্তি সেশন ও স্ট্যাটাস (Admission Status)"
        verbose_name_plural = "২. ভর্তি সেশন ও স্ট্যাটাস (Admission Status)"

    def __str__(self):
        status = "চালু" if self.is_open else "বন্ধ"
        return f"ভর্তি কার্যক্রম: {status} ({self.session_name})"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class PrayerTime(models.Model):
    is_active = models.BooleanField(
        default=True,
        verbose_name="হোমপেজে নামাজের সময়সূচি প্রদর্শন করবেন?",
        help_text="টিক চিহ্ন দেওয়া থাকলে হোমপেজে নামাজের জামা'আত কার্ড প্রদর্শিত হবে।"
    )
    title = models.CharField(
        max_length=150,
        default="দৈনিক জামা'আতের সময়সূচি",
        verbose_name="কার্ডের শিরোনাম"
    )
    sub_title = models.CharField(
        max_length=200,
        default="জামিয়া হুসাইনিয়া কেন্দ্রীয় মসজিদ",
        verbose_name="উপ-শিরোনাম / মসজিদ নাম"
    )
    fajr = models.CharField(max_length=20, default="৫:১৫ AM", verbose_name="ফজর জামা'আত")
    zuhr = models.CharField(max_length=20, default="১:৩০ PM", verbose_name="যোহর জামা'আত")
    asr = models.CharField(max_length=20, default="৪:৪৫ PM", verbose_name="আসর জামা'আত")
    maghrib = models.CharField(max_length=20, default="৬:০৫ PM", verbose_name="মাগরিব জামা'আত")
    isha = models.CharField(max_length=20, default="৮:০০ PM", verbose_name="এশা জামা'আত")
    jummah = models.CharField(max_length=20, default="১:৩০ PM", verbose_name="জুমু'আ জামা'আত")
    sehri_end = models.CharField(max_length=20, blank=True, default="৪:৪৫ AM", verbose_name="সাহরীর শেষ সময় (ঐচ্ছিক)")
    iftar = models.CharField(max_length=20, blank=True, default="৬:১০ PM", verbose_name="ইফতারের সময় (ঐচ্ছিক)")
    special_note = models.CharField(
        max_length=255,
        blank=True,
        default="ওয়াক্ত শুরুর ১০ মিনিট পর জামা'আত অনুষ্ঠিত হয়।",
        verbose_name="বিশেষ বিজ্ঞপ্তি / ফুটার নোট"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="সর্বশেষ আপডেট")

    class Meta:
        verbose_name = "৩. নামাজের সময়সূচি (Prayer Times)"
        verbose_name_plural = "৩. নামাজের সময়সূচি (Prayer Times)"

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class ContactSetting(models.Model):
    # Primary & Secondary Phone
    primary_phone = models.CharField(
        max_length=50,
        default="+8801751699909",
        verbose_name="প্রধান যোগাযোগ নম্বর (Primary Phone)",
        help_text="ওয়েবসাইটের হেডার, ফুটার ও নোটিশে প্রদর্শিত মূল নম্বর"
    )
    primary_phone_label = models.CharField(
        max_length=100,
        default="মাদরাসা অফিস ও তথ্য হেল্পলাইন",
        blank=True,
        verbose_name="প্রধান নম্বরের বিবরণ/লেবেল"
    )
    secondary_phone = models.CharField(
        max_length=50,
        blank=True,
        default="",
        verbose_name="বিকল্প/দ্বিতীয় ফোন নম্বর (Secondary Phone)",
        help_text="প্রয়োজনে দ্বিতীয় যোগাযোগ নম্বর যুক্ত করুন (ঐচ্ছিক)"
    )
    secondary_phone_label = models.CharField(
        max_length=100,
        default="জরুরি যোগাযোগ",
        blank=True,
        verbose_name="বিকল্প নম্বরের বিবরণ/লেবেল"
    )
    
    # WhatsApp
    whatsapp_number = models.CharField(
        max_length=50,
        default="+8801751699909",
        blank=True,
        verbose_name="হোয়াটসঅ্যাপ নম্বর (WhatsApp)",
        help_text="সরাসরি চ্যাট করতে কান্ট্রি কোডসহ দিন, যেমন: +8801751699909"
    )
    whatsapp_label = models.CharField(
        max_length=100,
        default="হোয়াটসঅ্যাপ হেল্পলাইন",
        blank=True,
        verbose_name="হোয়াটসঅ্যাপের বিবরণ/লেবেল"
    )

    # Mobile Financial Services (MFS / মোবাইল ব্যাংকিং)
    bkash_number = models.CharField(
        max_length=50,
        blank=True,
        default="01751699909",
        verbose_name="বিকাশ নম্বর (Bkash Number)",
        help_text="ফি প্রদান বা দানের বিকাশ নম্বর"
    )
    bkash_type = models.CharField(
        max_length=30,
        choices=[
            ('personal', 'পার্সোনাল (Personal)'),
            ('merchant', 'মার্চেন্ট (Merchant)'),
            ('agent', 'এজেন্ট (Agent)'),
        ],
        default='personal',
        verbose_name="বিকাশ অ্যাকাউন্ট টাইপ"
    )
    nagad_number = models.CharField(
        max_length=50,
        blank=True,
        default="",
        verbose_name="নগদ নম্বর (Nagad Number)",
        help_text="নগদ পেমেন্ট বা অনুদান নম্বর"
    )
    nagad_type = models.CharField(
        max_length=30,
        choices=[
            ('personal', 'পার্সোনাল (Personal)'),
            ('merchant', 'মার্চেন্ট (Merchant)'),
            ('agent', 'এজেন্ট (Agent)'),
        ],
        default='personal',
        verbose_name="নগদ অ্যাকাউন্ট টাইপ"
    )
    rocket_number = models.CharField(
        max_length=50,
        blank=True,
        default="",
        verbose_name="রকেট নম্বর (Rocket Number)",
        help_text="রকেট অ্যাকাউন্ট নম্বর (প্রয়োজনে)"
    )
    rocket_type = models.CharField(
        max_length=30,
        choices=[
            ('personal', 'পার্সোনাল (Personal)'),
            ('merchant', 'মার্চেন্ট (Merchant)'),
        ],
        default='personal',
        verbose_name="রকেট অ্যাকাউন্ট টাইপ"
    )

    # Emails
    primary_email = models.EmailField(
        default="jamiyahusainiya1@gmail.com",
        verbose_name="প্রধান ইমেইল ঠিকানা (Primary Email)",
        help_text="ওয়েবসাইটের হেডার, ফুটার ও নোটিশে প্রদর্শিত মূল ইমেইল"
    )
    primary_email_label = models.CharField(
        max_length=100,
        default="সাধারণ তথ্য ও অফিশিয়াল যোগাযোগ",
        blank=True,
        verbose_name="প্রধান ইমেইলের বিবরণ"
    )
    secondary_email = models.EmailField(
        blank=True,
        default="",
        verbose_name="বিকল্প / ভর্তি সংক্রান্ত ইমেইল (Secondary Email)",
        help_text="ভর্তি বা বিশেষ যোগাযোগের ইমেইল (ঐচ্ছিক)"
    )
    secondary_email_label = models.CharField(
        max_length=100,
        default="ভর্তি ও দাপ্তরিক যোগাযোগ",
        blank=True,
        verbose_name="বিকল্প ইমেইলের বিবরণ"
    )

    # Address & Hours
    address = models.TextField(
        default="শায়েস্তাগঞ্জ - হবিগঞ্জ রোড, কুটিরগাঁও রোড সংলগ্ন, শায়েস্তাগঞ্জ, হবিগঞ্জ",
        verbose_name="মাদরাসার পূর্ণাঙ্গ ঠিকানা (Address)"
    )
    office_hours = models.CharField(
        max_length=200,
        default="প্রতিদিন সকাল ৯:০০ হতে আসর এবং আসর হতে মাগরিব পর্যন্ত অফিস খোলা থাকে।",
        verbose_name="সাক্ষাৎ ও অফিস সময় (Office Hours)"
    )
    google_maps_url = models.TextField(
        blank=True,
        default="https://maps.app.goo.gl/rNkJg8y8g",
        verbose_name="গুগল ম্যাপ লোকেশন লিংক (Google Maps URL)"
    )

    # Social Media
    facebook_url = models.URLField(
        max_length=300,
        blank=True,
        default="https://facebook.com",
        verbose_name="ফেসবুক পেজ লিংক"
    )
    youtube_url = models.URLField(
        max_length=300,
        blank=True,
        default="https://youtube.com",
        verbose_name="ইউটিউব চ্যানেল লিংক"
    )

    updated_at = models.DateTimeField(auto_now=True, verbose_name="সর্বশেষ আপডেট")

    class Meta:
        verbose_name = "৪. যোগাযোগ ও হেল্পলাইন (Contact & Helpline)"
        verbose_name_plural = "৪. যোগাযোগ ও হেল্পলাইন (Contact & Helpline)"

    def __str__(self):
        return f"যোগাযোগ: {self.primary_phone} | {self.primary_email}"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
