from django.contrib import admin
from .models import StudentResults, StudentResultImage

class StudentResultsAdmin(admin.ModelAdmin):
    list_display = ['id', 'studentClassName', 'studentClassDescription', 'resultCreatedAt', 'resultUpdatedAt']

class StudentResultImageAdmin(admin.ModelAdmin):
    list_display = ['student_result', 'resultsSheetImg']

admin.site.register(StudentResults, StudentResultsAdmin)

admin.site.register(StudentResultImage, StudentResultImageAdmin)