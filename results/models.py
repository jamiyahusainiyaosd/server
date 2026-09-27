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
