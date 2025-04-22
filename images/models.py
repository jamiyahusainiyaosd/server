from django.db import models
import uuid

# Create your models here.
class Images(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    img = models.CharField(default='', max_length=2000)

    def __str__(self):
        return f'{self.img}'
    
    class Meta:
        verbose_name_plural = 'ইমেজ বা ছবি'