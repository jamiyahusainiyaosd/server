from rest_framework import generics
from rest_framework.filters import SearchFilter
from .models import FinanicialReport
from .serializers import FinanicialReportSerializers

class FinanicialReportListView(generics.ListAPIView):
    queryset = FinanicialReport.objects.all().order_by('-finanicialReportCreate')
    serializer_class = FinanicialReportSerializers
    filter_backends = [SearchFilter]
    search_fields = ['finanicialReportName']

class FinanicialReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FinanicialReport.objects.all()
    serializer_class = FinanicialReportSerializers