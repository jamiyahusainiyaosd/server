from django.contrib import admin
from .models import PhotoGallary, VideoGallary

class PhotoGallaryAdmin(admin.ModelAdmin):
    list_display = ['id', 'photoTitle', 'photoImg']

class VideoGallaryAdmin(admin.ModelAdmin):
    list_display = ['id', 'videoTitle', 'videoImg']

admin.site.register(PhotoGallary, PhotoGallaryAdmin)
admin.site.register(VideoGallary, VideoGallaryAdmin)