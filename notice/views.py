from rest_framework import generics
from .models import Notice
from .serializers import NoticeSerializer

class NoticeListApiView(generics.ListAPIView):
    serializer_class = NoticeSerializer

    def get_queryset(self):
        notice_type = self.kwargs.get('notice_type')
        print(f"Request Notice Type: {notice_type}")  

        if notice_type == 'recent':
            queryset = Notice.objects.filter(notice_type='Recent').order_by('-created_at')[:3]
            print(f"Filtered Recent Notices: {queryset}")  
            return queryset
        return Notice.objects.all()


class NoticeDetailsApiView(generics.RetrieveAPIView):
    serializer_class = NoticeSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        notice_type = self.kwargs.get('notice_type')
        print(f"Details API Notice Type: {notice_type}")  

        if notice_type == 'recent':
            queryset = Notice.objects.filter(notice_type='Recent')
        else:
            queryset = Notice.objects.all()

        print(f"Filtered Details Notice: {queryset}")  
        return queryset