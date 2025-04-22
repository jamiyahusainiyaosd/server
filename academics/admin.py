from django.contrib import admin
from .models import Academic

# Register your models here.
class AcademicAdmin(admin.ModelAdmin):
    list_display = ['id', 'class_name', 'class_title', 'class_description', 'student_count', 'number_seat', 'class_created', 'class_update']
    search_fields = ['class_name', 'class_title']

admin.site.register(Academic, AcademicAdmin)