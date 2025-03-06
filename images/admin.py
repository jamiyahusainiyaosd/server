from django.contrib import admin
from .models import Images
# Register your models here.
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'img']

admin.site.register(Images, ImageAdmin)

