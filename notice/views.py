from rest_framework import generics
from .models import Notice
from .serializers import NoticeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

class NoticeListApiView(generics.ListAPIView):
    queryset = Notice.objects.filter(notice_type='Recent').order_by('-created_at')[:3]
    serializer_class = NoticeSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['notice_type', 'title']
    ordering_fields = ['id']

class NoticeDetailsApiView(generics.RetrieveAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    lookup_field = 'pk'