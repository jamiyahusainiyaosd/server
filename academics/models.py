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

    # প্রধান বৈশিষ্ট্য ও বিষয়সূচি (৪টি কার্ড)
    feature_1_title = models.CharField(max_length=150, blank=True, default='', verbose_name='বৈশিষ্ট্য ১: শিরোনাম')
    feature_1_desc = models.CharField(max_length=255, blank=True, default='', verbose_name='বৈশিষ্ট্য ১: বিবরণ')
    feature_2_title = models.CharField(max_length=150, blank=True, default='', verbose_name='বৈশিষ্ট্য ২: শিরোনাম')
    feature_2_desc = models.CharField(max_length=255, blank=True, default='', verbose_name='বৈশিষ্ট্য ২: বিবরণ')
    feature_3_title = models.CharField(max_length=150, blank=True, default='', verbose_name='বৈশিষ্ট্য ৩: শিরোনাম')
    feature_3_desc = models.CharField(max_length=255, blank=True, default='', verbose_name='বৈশিষ্ট্য ৩: বিবরণ')
    feature_4_title = models.CharField(max_length=150, blank=True, default='', verbose_name='বৈশিষ্ট্য ৪: শিরোনাম')
    feature_4_desc = models.CharField(max_length=255, blank=True, default='', verbose_name='বৈশিষ্ট্য ৪: বিবরণ')

    # দৈনিক ক্লাস রুটিন (৩টি অধিবেশন)
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
