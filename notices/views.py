from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import Notice
from .serializers import NoticeDetailsSerializer, NoticeListSerializer

class CustomPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 100

class NoticeListApiView(generics.ListAPIView):
    serializer_class = NoticeListSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Notice.objects.all().order_by('-created_at')

class NoticeDetailsApiView(generics.RetrieveAPIView):
    serializer_class = NoticeDetailsSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Notice.objects.all()

class LatestNoticesApiView(generics.ListAPIView):
    serializer_class = NoticeListSerializer

    def get_queryset(self):
        return Notice.objects.order_by('-created_at')[:3]