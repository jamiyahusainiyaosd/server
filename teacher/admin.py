from django.contrib import admin
from .models import TeacherModel

# Register your models here.
class TeacherModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'designation', 'phone_number', 'created_at', 'updated_at']
    search_fields = ['name', 'designation', 'phone_number']
    list_filter = ['designation']

admin.site.register(TeacherModel, TeacherModelAdmin)