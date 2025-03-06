from rest_framework import serializers
from .models import Admission

class AdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admission
        fields = ['id', 'ClassName', 'class_level', 'form_fee', 'new_admission_fee', 'old_admission_fee', 'new_total_fee', 'old_total_fee', 'additional_fee', 'monthly_fee', 'admission_start_date', 'admission_end_date', 'required_documents', 'seat_availability', 'admission_created', 'admission_updated']