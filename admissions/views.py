from rest_framework import generics, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Admission, AdmissionRule
from .serializers import AdmissionSerializer, AdmissionRuleSerializer
from theme_config.models import AdmissionStatus
from theme_config.serializers import AdmissionStatusSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

class AdmissionPagination(PageNumberPagination):
    page_size = 9 
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

class AdmissionRuleListView(generics.ListCreateAPIView):
    queryset = AdmissionRule.objects.filter(is_active=True).order_by('order', 'created_at')
    serializer_class = AdmissionRuleSerializer
    pagination_class = None

class AdmissionStatusView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        obj = AdmissionStatus.get_solo()
        serializer = AdmissionStatusSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
