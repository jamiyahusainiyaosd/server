from django.db import models

class Notice(models.Model):
    title = models.CharField(max_length=1000, verbose_name='নোটিশ এর নাম')
    description = models.TextField(blank=True, null=True, verbose_name='নোটিশ এর বিস্তারিত')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'  

    class Meta:
        verbose_name_plural = 'সব নোটিশ'