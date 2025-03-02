from django.db import models

# Create your models here.
class Images(models.Model):
    img = models.CharField(default='', max_length=1000)