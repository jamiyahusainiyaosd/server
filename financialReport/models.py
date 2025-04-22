from django.db import models
import uuid

class FinanicialReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    finanicialReportName = models.CharField(max_length=500)
    finanicialReportDescription = models.TextField()
    finanicialReportImage = models.CharField(max_length=2000, default='')
    finanicialReportCreate = models.DateTimeField(auto_now_add=True)
    finanicialReportUpdate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.finanicialReportName}'
    
    class Meta:
        verbose_name_plural = 'আর্থিক প্রতিবেদন'