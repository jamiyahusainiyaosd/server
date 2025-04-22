from django.db import models
import uuid

class BookIntroduction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bookTitle = models.CharField(max_length=300)
    bookDescription = models.TextField()
    authorName = models.CharField(max_length=200)
    bookKobarImg = models.CharField(max_length=2000, default='')
    bookCreatedAt = models.DateTimeField(auto_now_add=True)
    bookUpdatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.bookTitle}'
    
    class Meta:
        verbose_name_plural = 'বুজুর্গানে দ্বীনের বই পরিচিতি'