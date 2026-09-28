from django.db import models
import uuid

class Academic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class_name = models.CharField(max_length=100, verbose_name='ক্লাসের নাম')
    class_title = models.CharField(max_length=255, verbose_name='ক্লাসের একটি টাইটেল')
    class_description = models.TextField(verbose_name='ক্লাসের সম্পর্কে বিস্তারিত')
    category = models.CharField(max_length=100, default='কিতাব বিভাগ', blank=True, verbose_name='বিভাগ / স্তর (যেমন: নূরানী ও মক্তব, হিফজুল কুরআন, কিতাব বিভাগ)')
    course_code = models.CharField(max_length=50, blank=True, default='', verbose_name='কোর্স / ক্লাস কোড (ঐচ্ছিক)')
    admission_status = models.CharField(max_length=50, default='ভর্তি চলমান', blank=True, verbose_name='ভর্তি স্থিতি (যেমন: ভর্তি চলমান / আসন পূর্ণ)')
    academic_year = models.CharField(max_length=100, default='২০২৫ — ২০২৬', blank=True, verbose_name='শিক্ষাবর্ষ')
    routine_badge = models.CharField(max_length=100, default='নিয়মিত পাঠ ও তাকরার', blank=True, verbose_name='রুটিন ব্যাজ (যেমন: ৩ পালা পাঠদান)')
    teacher_note = models.TextField(blank=True, default='', verbose_name='উস্তাদদের দিকনির্দেশনা ও তত্ত্বাবধান নোট')
    student_count = models.IntegerField(default=0, verbose_name='বর্তমান ছাত্র সংখ্যা')
    number_seat = models.IntegerField(default=0, verbose_name='মোট আসন সংখ্যা')

    feature_1_title = models.CharField(max_length=150, blank=True, default='', verbose_name='বৈশিষ্ট্য ১: শিরোনাম')
    feature_1_desc = models.CharField(max_length=255, blank=True, default='', verbose_name='বৈশিষ্ট্য ১: বিবরণ')
    feature_2_title = models.CharField(max_length=150, blank=True, default='', verbose_name='বৈশিষ্ট্য ২: শিরোনাম')
    feature_2_desc = models.CharField(max_length=255, blank=True, default='', verbose_name='বৈশিষ্ট্য ২: বিবরণ')
    feature_3_title = models.CharField(max_length=150, blank=True, default='', verbose_name='বৈশিষ্ট্য ৩: শিরোনাম')
    feature_3_desc = models.CharField(max_length=255, blank=True, default='', verbose_name='বৈশিষ্ট্য ৩: বিবরণ')
    feature_4_title = models.CharField(max_length=150, blank=True, default='', verbose_name='বৈশিষ্ট্য ৪: শিরোনাম')
    feature_4_desc = models.CharField(max_length=255, blank=True, default='', verbose_name='বৈশিষ্ট্য ৪: বিবরণ')

    routine_1_time = models.CharField(max_length=100, blank=True, default='', verbose_name='১ম অধিবেশন সময়')
    routine_1_title = models.CharField(max_length=200, blank=True, default='', verbose_name='১ম অধিবেশন পাঠ')
    routine_2_time = models.CharField(max_length=100, blank=True, default='', verbose_name='২য় অধিবেশন সময়')
    routine_2_title = models.CharField(max_length=200, blank=True, default='', verbose_name='২য় অধিবেশন পাঠ')
    routine_3_time = models.CharField(max_length=100, blank=True, default='', verbose_name='৩য় অধিবেশন সময়')
    routine_3_title = models.CharField(max_length=200, blank=True, default='', verbose_name='৩য় অধিবেশন পাঠ')

    class_created = models.DateTimeField(auto_now_add=True)
    class_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.class_name} - {self.class_title}'
    
    class Meta:
        verbose_name_plural = 'একাডেমিক জামাত ও পাঠ্যক্রম'


class BoardingRule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rule_number = models.PositiveIntegerField(default=1, verbose_name='ক্রমিক নম্বর')
    category = models.CharField(max_length=50, default='general', verbose_name='ক্যাটাগরি আইডি (general, dining, leave, worship, prohibitions)')
    category_label = models.CharField(max_length=100, default='সাধারণ আচরণ ও শৃংখলা', verbose_name='ক্যাটাগরি নাম')
    rule_text = models.TextField(verbose_name='নীতিমালা / নির্দেশনার বিবরণ')
    importance = models.CharField(max_length=50, default='বাধ্যতামূলক', verbose_name='গুরুত্ব স্তর')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['rule_number']
        verbose_name = 'আবাসিক নীতিমালা'
        verbose_name_plural = '১. আবাসিক নীতিমালা (Boarding Rules)'

    def __str__(self):
        return f'{self.rule_number}. {self.rule_text[:50]}'


class Holiday(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.PositiveIntegerField(default=1, verbose_name='ক্রমিক নম্বর')
    title = models.CharField(max_length=255, verbose_name='ছুটির বিবরণ / পর্ব')
    category = models.CharField(max_length=100, default='ইসলামিক ছুটি', verbose_name='ছুটির ধরন')
    academic_year = models.CharField(max_length=50, default='2025-2026', verbose_name='শিক্ষাবর্ষ')
    date_range = models.CharField(max_length=150, verbose_name='তারিখ')
    hijri_date = models.CharField(max_length=150, blank=True, default='', verbose_name='হিজরী তারিখ')
    day_name = models.CharField(max_length=100, verbose_name='বারের নাম')
    duration = models.CharField(max_length=50, default='০১ দিন', verbose_name='দিনের সংখ্যা')
    reopen_date = models.CharField(max_length=150, verbose_name='মাদরাসা খোলার তারিখ')
    note = models.CharField(max_length=255, blank=True, default='', verbose_name='মন্তব্য')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'ছুটির তালিকা'
        verbose_name_plural = '২. ছুটির তালিকা (Holiday Calendar)'

    def __str__(self):
        return f'{self.order}. {self.title} ({self.duration})'


class ExamSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_id = models.CharField(max_length=50, unique=True, verbose_name='সেশন আইডি (annual, befaq, term1, term2)')
    name = models.CharField(max_length=150, verbose_name='পরীক্ষার সেশন নাম')
    badge = models.CharField(max_length=100, default='আসন্ন প্রধান পরীক্ষা', verbose_name='ব্যাজ')
    order = models.PositiveIntegerField(default=1, verbose_name='ক্রমিক')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'পরীক্ষার সেশন'
        verbose_name_plural = '৩.১ পরীক্ষার সেশন (Exam Sessions)'

    def __str__(self):
        return f'{self.name} ({self.session_id})'


class ExamRoutine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_id = models.CharField(max_length=50, default='annual', verbose_name='সেশন আইডি (annual, befaq, term1, term2)')
    session_name = models.CharField(max_length=150, default='বার্ষিক শালানা ইমতিহান ২০২৬', verbose_name='পরীক্ষার সেশন নাম')
    academic_year = models.CharField(max_length=100, default='২০২৫-২০২৬ শিক্ষাবর্ষ', verbose_name='শিক্ষাবর্ষ')
    jamat_id = models.CharField(max_length=50, default='meshkat', verbose_name='জামাত আইডি')
    jamat_name = models.CharField(max_length=150, verbose_name='জামাতের নাম')
    date_str = models.CharField(max_length=100, verbose_name='পরীক্ষার তারিখ')
    day_name = models.CharField(max_length=50, verbose_name='বার')
    subject = models.CharField(max_length=255, verbose_name='বিষয় / কিতাবের নাম')
    subject_code = models.CharField(max_length=50, blank=True, default='', verbose_name='বিষয় কোড')
    time_str = models.CharField(max_length=100, default='সকাল ৯:০০ – ১২:০০', verbose_name='পরীক্ষার সময়')
    hall_name = models.CharField(max_length=150, default='হল নং ০১ (দারুল হাদীস মিলনায়তন)', verbose_name='হল / কক্ষ')
    marks = models.CharField(max_length=20, default='১০০', verbose_name='পূর্ণমান')
    order = models.PositiveIntegerField(default=1, verbose_name='ক্রমিক')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['session_id', 'order']
        verbose_name = 'পরীক্ষার রুটিন'
        verbose_name_plural = '৩.২ পরীক্ষার রুটিন (Exam Routine)'

    def __str__(self):
        return f'{self.session_name} - {self.jamat_name}: {self.subject}'


class ExamInstruction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.PositiveIntegerField(default=1, verbose_name='ক্রমিক নম্বর')
    instruction = models.TextField(verbose_name='পরীক্ষার্থীদের জন্য বিশেষ নির্দেশনা')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'পরীক্ষার্থীদের নির্দেশাবলী'
        verbose_name_plural = '৩.৩ পরীক্ষার্থীদের বিশেষ নির্দেশাবলী (Exam Instructions)'

    def __str__(self):
        return f'{self.order}. {self.instruction[:60]}'


class ClassDepartment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dept_id = models.CharField(max_length=50, unique=True, verbose_name='বিভাগ আইডি (kitab, hifz, noorani)')
    name = models.CharField(max_length=150, verbose_name='বিভাগের নাম')
    desc = models.CharField(max_length=255, verbose_name='সংক্ষিপ্ত স্তর বিবরণ')
    icon = models.CharField(max_length=50, default='menu_book', verbose_name='আইকন')
    order = models.PositiveIntegerField(default=1, verbose_name='ক্রমিক')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'ক্লাস রুটিন বিভাগ'
        verbose_name_plural = '৪.১ রুটিন বিভাগসমূহ (Class Departments)'

    def __str__(self):
        return f'{self.name} ({self.dept_id})'


class ClassRoutine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department = models.CharField(max_length=50, default='kitab', verbose_name='বিভাগ আইডি (kitab, hifz, noorani)')
    department_name = models.CharField(max_length=150, default='কিতাব বিভাগ', verbose_name='বিভাগের নাম')
    jamat_id = models.CharField(max_length=50, default='meshkat', verbose_name='জামাত আইডি')
    jamat_name = models.CharField(max_length=150, default='ফযিলত ২য় বর্ষ (মেশকাত)', verbose_name='জামাতের নাম')
    period = models.CharField(max_length=50, verbose_name='পিরিয়ড / ঘণ্টা')
    time_slot = models.CharField(max_length=100, verbose_name='সময়কাল')
    subject = models.CharField(max_length=255, verbose_name='বিষয় / কিতাবের নাম')
    teacher = models.CharField(max_length=150, blank=True, default='—', verbose_name='পাঠদানকারী সম্মানিত উস্তাদ')
    room = models.CharField(max_length=100, blank=True, default='ফযিলত হল-১', verbose_name='কক্ষ / হল')
    is_break = models.BooleanField(default=False, verbose_name='বিরতি কিনা')
    order = models.PositiveIntegerField(default=1, verbose_name='ক্রমিক')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['department', 'jamat_id', 'order']
        verbose_name = 'ক্লাস রুটিন'
        verbose_name_plural = '৪.২ ক্লাস রুটিন (Class Routine)'

    def __str__(self):
        return f'{self.department_name} ({self.jamat_name}) - {self.period}: {self.subject}'


class DailySchedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.PositiveIntegerField(default=1, verbose_name='ক্রমিক নম্বর')
    time_slot = models.CharField(max_length=100, verbose_name='সময়কাল (যেমন: ৪:১৫ – ৫:০০)')
    title = models.CharField(max_length=200, verbose_name='শিরোনাম / পর্বের নাম')
    description = models.TextField(verbose_name='বিবরণ')
    badge = models.CharField(max_length=100, default='আমল ও ইবাদত', verbose_name='ব্যাজ')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = '২৪ ঘণ্টার সুন্নতি রুটিন'
        verbose_name_plural = '৪.৩ ২৪ ঘণ্টার সুন্নতি রুটিন (Daily Sunnah Routine)'

    def __str__(self):
        return f'{self.order}. {self.time_slot}: {self.title}'


class CoCurricularActivity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_id = models.CharField(max_length=50, unique=True, verbose_name='অ্যাক্টিভিটি আইডি')
    title = models.CharField(max_length=255, verbose_name='কার্যক্রমের শিরোনাম')
    short_desc = models.TextField(verbose_name='সংক্ষিপ্ত বিবরণ')
    full_desc = models.TextField(blank=True, default='', verbose_name='পূর্ণাঙ্গ বিবরণ')
    category = models.CharField(max_length=50, default='language', verbose_name='ক্যাটাগরি আইডি')
    category_label = models.CharField(max_length=100, default='ভাষা ও সাহিত্য', verbose_name='ক্যাটাগরি লেবেল')
    timing = models.CharField(max_length=150, verbose_name='সময়সূচি')
    venue = models.CharField(max_length=150, verbose_name='স্থান')
    mentor = models.CharField(max_length=255, verbose_name='দায়িত্বপ্রাপ্ত উস্তাদ')
    badge = models.CharField(max_length=100, default='সাপ্তাহিক ফোরাম', verbose_name='ব্যাজ')
    icon = models.CharField(max_length=50, default='record_voice_over', verbose_name='আইকন')
    items_json = models.TextField(blank=True, default='[]', verbose_name='বৈশিষ্ট্য তালিকা (JSON Array)')
    order = models.PositiveIntegerField(default=1, verbose_name='ক্রমিক')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'সহ-পাঠ্যক্রমিক কার্যক্রম'
        verbose_name_plural = '৫. সহ-পাঠ্যক্রমিক কার্যক্রম (Co-curricular Activities)'

    def __str__(self):
        return f'{self.order}. {self.title}'


class BoardingMealMenu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    day_key = models.CharField(max_length=20, unique=True, verbose_name='বারের কি (sat, sun, mon, tue, wed, thu, fri)')
    day_name = models.CharField(max_length=50, verbose_name='বার (যেমন: শনিবার)')
    breakfast = models.CharField(max_length=255, verbose_name='সকালের খাবার (নাস্তা)')
    lunch = models.CharField(max_length=255, verbose_name='দুপুরের খাবার')
    dinner = models.CharField(max_length=255, verbose_name='রাতের খাবার')
    special_note = models.CharField(max_length=255, blank=True, default='প্রতি বেলা তরকারীর সাথে মুসুরীর ডাল থাকবে।', verbose_name='বিশেষ দ্রষ্টব্য / টীকা')
    order = models.PositiveIntegerField(default=1, verbose_name='ক্রমিক (১-৭)')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'আবাসিক খাবার মেনু'
        verbose_name_plural = '৬.১ আবাসিক শিক্ষার্থীদের দৈনিক খাবার তালিকা (Boarding Meal Menu)'

    def __str__(self):
        return f'{self.day_name}: সকাল ({self.breakfast}), দুপুর ({self.lunch}), রাত ({self.dinner})'


class BoardingMealTiming(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meal_type = models.CharField(max_length=100, verbose_name='আহারের বেলা (যেমন: সকালের নাস্তা)')
    time_slot = models.CharField(max_length=100, verbose_name='পরিবেশনের সময়কাল (যেমন: সকাল ৭:৩০ – ৮:০০)')
    icon = models.CharField(max_length=50, default='restaurant', verbose_name='আইকন')
    details = models.TextField(blank=True, default='', verbose_name='বিবরণ / নির্দেশনা')
    order = models.PositiveIntegerField(default=1, verbose_name='ক্রমিক')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'খাবারের সময়সূচি'
        verbose_name_plural = '৬.২ খাবার পরিবেশন সময়সূচি (Meal Timings)'

    def __str__(self):
        return f'{self.meal_type} ({self.time_slot})'


class BoardingMealRule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.PositiveIntegerField(default=1, verbose_name='ক্রমিক')
    rule_text = models.TextField(verbose_name='খাবার ও ডাইনিং সংক্রান্ত নীতিমালা')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'ডাইনিং নীতিমালা'
        verbose_name_plural = '৬.৩ ডাইনিং ও খাবার নীতিমালা (Dining Guidelines)'

    def __str__(self):
        return f'{self.order}. {self.rule_text[:60]}'
