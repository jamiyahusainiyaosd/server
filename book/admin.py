from django.contrib import admin
from .models import BookIntroduction

class BookIntroductionAdmin(admin.ModelAdmin):
    list_display = ['id', 'bookTitle', 'bookDescription', 'authorName', 'bookKobarImg', 'bookCreatedAt', 'bookUpdatedAt']

admin.site.register(BookIntroduction, BookIntroductionAdmin)