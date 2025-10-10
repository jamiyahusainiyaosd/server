# views.py
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from .models import PhotoGallary, VideoGallary
from .serializers import PhotoGallarySerializers, VideoGallarySerializers

class CustomPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 100

class PhotoGallaryListView(generics.ListAPIView):
    queryset = PhotoGallary.objects.all().order_by('-id')
    serializer_class = PhotoGallarySerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['photoTitle']
    pagination_class = CustomPagination

class PhotoGallaryDetailView(generics.RetrieveDestroyAPIView):
    queryset = PhotoGallary.objects.all()
    serializer_class = PhotoGallarySerializers
    lookup_field = 'id'

class VideoGallaryListView(generics.ListAPIView):
    queryset = VideoGallary.objects.all().order_by('-id')
    serializer_class = VideoGallarySerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['videoTitle']
    pagination_class = CustomPagination

class VideoGallaryDetailView(generics.RetrieveDestroyAPIView):
    queryset = VideoGallary.objects.all()
    serializer_class = VideoGallarySerializers
    lookup_field = 'id'