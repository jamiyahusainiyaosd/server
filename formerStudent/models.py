import uuid
from django.db import models

class FormerStudent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    image = models.URLField(default='', blank=True, null=True, verbose_name='ছবি') 
    name = models.CharField(max_length=150, verbose_name='নাম')
    address = models.CharField(max_length=255, verbose_name='ঠিকানা')
    pass_year = models.PositiveIntegerField(blank=True, null=True, verbose_name='পাস বছর')  
    current = models.CharField(max_length=255, verbose_name='বর্তমান অবস্থা')
    mobile = models.CharField(max_length=20, verbose_name='মোবাইল')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'সাবেক-ছাত্র'
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["mobile"]),
            models.Index(fields=["pass_year"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.mobile})"