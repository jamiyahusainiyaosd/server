from django.db import models
import uuid

class StudentResults(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    studentClassName = models.CharField(max_length=1000)
    studentClassDescription = models.TextField()
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