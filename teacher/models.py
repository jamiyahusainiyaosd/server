from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class TeacherModel(models.Model):
    name = models.CharField(max_length=150, verbose_name='শিক্ষকের নাম')
    designation = models.CharField(max_length=100, verbose_name='শিক্ষকের পদবী')
    phone_number = models.CharField(
        max_length=16,
        verbose_name='শিক্ষকের ফোন নাম্বার',
        validators=[RegexValidator(regex=r'^\+?\d{9,15}$', message='Enter A Valid Phone Number.')]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'শিক্ষক'