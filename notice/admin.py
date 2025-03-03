from django.contrib import admin
from .models import Notice

# Register your models here.
class NoticeAdmin(admin.ModelAdmin):
    list_display =  ['id', 'title', 'description', 'created_at', 'updated_at']

admin.site.register(Notice, NoticeAdmin)