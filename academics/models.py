from django.db import models
import uuid

# Create your models here.
class Academic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class_name = models.CharField(max_length=100, verbose_name='ক্লাসের নাম')
    class_title = models.CharField(max_length=100, verbose_name='ক্লাসের একটি টাইটেল')
    class_description = models.TextField(verbose_name='ক্লাসের সম্পর্কে বিস্তারিত')
    student_count  = models.IntegerField(default=0, verbose_name='ছাত্রদের গগণা')
    number_seat  = models.IntegerField(default=0, verbose_name='আশন গণনা')
    class_created = models.DateTimeField(auto_now_add=True)
    class_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.class_name} - {self.class_title}'
    
    class Meta:
        verbose_name_plural = 'শিক্ষাবিদগণ'