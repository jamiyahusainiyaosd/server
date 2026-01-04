from django.contrib import admin
from .models import FormerStudent

class FormerStudentAdmin(admin.ModelAdmin):
    list_display = ("image", "name", "address", "mobile", "pass_year", "created_at", "updated_at")
    search_fields = ("name", "mobile", "address", "current")
    list_filter = ("pass_year",)
    ordering = ("-created_at",)

admin.site.register(FormerStudent, FormerStudentAdmin)