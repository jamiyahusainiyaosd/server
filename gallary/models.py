from django.db import models
import uuid

class PhotoGallary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photoTitle = models.CharField(max_length=300, null=True, blank=True)
    photoImg = models.CharField(max_length=2000, default='')

    def __str__(self):
        return f'{self.photoTitle}'
    
    class Meta:
        verbose_name_plural = 'ফটো গ্যালারি'

class VideoGallary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    videoTitle = models.CharField(max_length=300, null=True, blank=True)
    videoImg = models.CharField(max_length=2000, default='')

    def __str__(self):
        return f'{self.videoTitle}'
    
    class Meta:
        verbose_name_plural = 'ভিডিও গ্যালারি'