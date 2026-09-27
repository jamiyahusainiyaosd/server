from django.db import models
import uuid

class Notice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=1000, verbose_name='নোটিশ এর নাম')
    description = models.TextField(blank=True, null=True, verbose_name='নোটিশ এর বিস্তারিত')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'  

    class Meta:
        verbose_name_plural = 'সব নোটিশ'


class Announcement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=500, verbose_name='ঘোষণা / বার্তা / জরুরি নম্বর')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    order = models.PositiveIntegerField(default=1, verbose_name='ক্রম (Order)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.text[:50]}'

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'স্ক্রলিং ঘোষণা (Marquee)'
        verbose_name_plural = 'স্ক্রলিং ঘোষণা সমূহ (Marquee)'
