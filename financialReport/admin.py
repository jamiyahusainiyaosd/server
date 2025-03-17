from django.contrib import admin
from .models import FinanicialReport

class FinanicialReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'finanicialReportName', 'finanicialReportDescription', 'finanicialReportImage', 'finanicialReportCreate','finanicialReportUpdate']

admin.site.register(FinanicialReport, FinanicialReportAdmin)