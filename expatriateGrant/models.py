import uuid
from django.db import models

class ExpatriateGrant(models.Model):
    class MemberType(models.TextChoices):
        PROBASHI = "প্রবাসী"

    class Status(models.TextChoices):
        ACTIVE = "সক্রিয়"
        INACTIVE = "নিষ্ক্রিয়"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    image = models.URLField(default='', blank=True, null=True, max_length=2000, verbose_name='ছবি')  
    name = models.CharField(max_length=150, verbose_name='নাম')
    address = models.CharField(max_length=255, verbose_name='ঠিকানা')
    mobile = models.CharField(max_length=20, verbose_name='মোবাইল')

    member_type = models.CharField(max_length=30, choices=MemberType.choices, default=MemberType.PROBASHI, verbose_name='সদস্যের ধরন')
    chadar_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='চাদার পরিমান')
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.ACTIVE, verbose_name='অবস্থা')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'প্রবাসীদের অনুদান'
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["mobile"]),
            models.Index(fields=["member_type"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.member_type})"