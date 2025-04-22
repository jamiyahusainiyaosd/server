from rest_framework import generics
from .models import Notice
from .serializers import NoticeDetailsSerializer, NoticeListSerializer

class NoticeListApiView(generics.ListAPIView):
    serializer_class = NoticeListSerializer

    def get_queryset(self):
        return Notice.objects.all()


class NoticeDetailsApiView(generics.RetrieveAPIView):
    serializer_class = NoticeDetailsSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Notice.objects.all()


class LatestNoticesApiView(generics.ListAPIView):
    serializer_class = NoticeListSerializer

    def get_queryset(self):
        return Notice.objects.order_by('-created_at')[:3]