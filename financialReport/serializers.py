from rest_framework import serializers
from .models import FinanicialReport

class FinanicialReportSerializers(serializers.ModelSerializer):
    class Meta:
        model = FinanicialReport
        fields = ['id', 'finanicialReportName', 'finanicialReportDescription', 'finanicialReportImage', 'finanicialReportCreate','finanicialReportUpdate']