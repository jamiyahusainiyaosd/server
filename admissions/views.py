from rest_framework import generics, filters
from .models import Admission
from .serializers import AdmissionSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

class AdmissionPagination(PageNumberPagination):
    page_size = 5 # প্রতিটি পেজের মধ্যে ৫ টি করে আইটেম দেখাবে।
    page_size_query_param = 'page_size'
    max_page_size = 100

class AdmissionListCreateView(generics.ListCreateAPIView):
    queryset = Admission.objects.all().order_by('-admission_created')
    serializer_class = AdmissionSerializer
    pagination_class = AdmissionPagination

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['class_level', 'seat_availability']
    search_fields = ['ClassName']
    ordering_fields = ['admission_start_date', 'admission_end_date']

class AdmissionDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer