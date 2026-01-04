from django.contrib import admin
from .models import ExpatriateGrant

class ExpatriateGrantAdmin(admin.ModelAdmin):
    list_display = ("image", "name", "mobile", "member_type", "status", "chadar_amount", "created_at", "updated_at")
    search_fields = ("name", "mobile", "address")
    list_filter = ("member_type", "status")
    ordering = ("-created_at",)

admin.site.register(ExpatriateGrant, ExpatriateGrantAdmin)