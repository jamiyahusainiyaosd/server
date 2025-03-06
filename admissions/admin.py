from django.contrib import admin
from .models import Admission
# Register your models here.

class AdmissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'ClassName', 'class_level', 'form_fee', 'new_admission_fee', 'old_admission_fee', 'new_total_fee', 'old_total_fee', 'additional_fee', 'monthly_fee', 'admission_start_date', 'admission_end_date', 'required_documents', 'seat_availability', 'admission_created', 'admission_updated']
    
    search_fields = ['ClassName', 'class_level']

    list_filter = ['class_level', 'seat_availability', 'admission_start_date']

admin.site.register(Admission, AdmissionAdmin)