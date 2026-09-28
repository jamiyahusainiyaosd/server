from django.db import models
import uuid

class StudentResults(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    studentClassName = models.CharField(max_length=1000, verbose_name='ক্লাসের নাম')
    studentClassDescription = models.TextField(verbose_name='ফলাফলের বিবরণ')
    exam_session = models.CharField(max_length=255, default='বার্ষিক শালানা ইমতিহান ২০২৬ — অনুমোদিত', blank=True, verbose_name='পরীক্ষার সেশন / নাম')
    academic_year = models.CharField(max_length=100, default='২০২৫ — ২০২৬', blank=True, verbose_name='শিক্ষাবর্ষ')
    board_name = models.CharField(max_length=255, default='শায়েস্তাগঞ্জ কেন্দ্রীয় নূরানী ও কওমি শিক্ষাবোর্ড', blank=True, verbose_name='শিক্ষাবোর্ড / পরিচালনাকারী')
    total_students = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='মোট পরীক্ষার্থী সংখ্যা')
    passed_students = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='উত্তীর্ণ শিক্ষার্থীর সংখ্যা')
    pass_rate = models.CharField(max_length=50, default='', blank=True, verbose_name='পাসের হার (যেমন: ৯৩%)')
    grade_detail = models.CharField(max_length=100, default='মুমতাজ ও জায়্যিদ', blank=True, verbose_name='মেধা গ্রেড / ফলাফল মান')
    certificate_status = models.CharField(max_length=100, default='অনুমোদিত', blank=True, verbose_name='সনদপত্র স্ট্যাটাস')
    helpline = models.CharField(max_length=50, default='+880 1751 699909', blank=True, verbose_name='পরীক্ষা দপ্তর হেল্পলাইন নম্বর')
    resultCreatedAt = models.DateTimeField(auto_now_add=True)
    resultUpdatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.studentClassName

    class Meta:
        verbose_name_plural = 'ছাত্রদের ফলাফল প্রকাশ'


class StudentResultImage(models.Model):
    student_result = models.ForeignKey(StudentResults, related_name='images', on_delete=models.CASCADE)
    resultsSheetImg = models.CharField(max_length=2000, default='', null=True, blank=True)
    resultSheetUpdatedAt = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'Image For {self.student_result.studentClassName}'
    
    class Meta:
        verbose_name_plural = 'ছাত্রদের ফলাফল ছবি'


class TopAchiever(models.Model):
    CATEGORY_CHOICES = [
        ('national', 'জাতীয় / দেশ সেরা'),
        ('division', 'বিভাগীয় সেরা'),
        ('district', 'জেলা ভিত্তিক সেরা'),
        ('madrasa', 'মাদ্রাসার অভ্যন্তরীণ সেরা'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, verbose_name='কৃতি শিক্ষার্থীর নাম')
    image = models.URLField(max_length=1000, blank=True, default='', verbose_name='ছবি (Supabase CDN URL)')
    class_name = models.CharField(max_length=150, verbose_name='জামাত / বিভাগ')
    achievement_title = models.CharField(max_length=200, verbose_name='মেধা স্থান / অর্জনের বিবরণ')
    board_name = models.CharField(
        max_length=200, 
        default='বেফাকুল মাদারিসিল আরাবিয়া বাংলাদেশ', 
        blank=True, 
        verbose_name='বোর্ড / পরীক্ষার নাম'
    )
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES, 
        default='national', 
        verbose_name='অর্জন স্তর / ক্যাটাগরি'
    )
    roll_number = models.CharField(max_length=50, blank=True, default='', verbose_name='রোল / নিবন্ধন নং')
    academic_year = models.CharField(max_length=100, default='২০২৫-২০২৬ ইং', blank=True, verbose_name='শিক্ষাবর্ষ / সন')
    score_or_division = models.CharField(
        max_length=100, 
        default='মুমতাজ (স্টার মার্কসহ)', 
        blank=True, 
        verbose_name='প্রাপ্ত গ্রেড / বিভাগ'
    )
    father_name = models.CharField(max_length=150, blank=True, default='', verbose_name='পিতার নাম')
    address = models.CharField(max_length=200, blank=True, default='', verbose_name='ঠিকানা / জেলা')
    quote = models.TextField(blank=True, default='', verbose_name='উস্তাদদের দোয়া ও অনুভূতি / মন্তব্য')
    is_featured = models.BooleanField(default=True, verbose_name='হোম পেজে "এ বছরের সেরা" হিসেবে প্রদর্শন করুন')
    order = models.PositiveIntegerField(default=1, verbose_name='প্রদর্শনের ক্রম (Order)')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'এ বছরের সেরা কৃতি শিক্ষার্থী'
        verbose_name_plural = 'এ বছরের সেরা কৃতি শিক্ষার্থীবৃন্দ'
        ordering = ['order', '-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['academic_year']),
        ]

    def __str__(self):
        return f'{self.name} — {self.achievement_title} ({self.class_name})'
