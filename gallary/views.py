from rest_framework import generics, filters
from .models import PhotoGallary, VideoGallary
from .serializers import PhotoGallarySerializers, VideoGallarySerializers

class PhotoGallaryListView(generics.ListAPIView):
    queryset = PhotoGallary.objects.all().order_by('-id')
    serializer_class = PhotoGallarySerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['photoTitle']

class PhotoGallaryDetailView(generics.RetrieveDestroyAPIView):
    queryset = PhotoGallary.objects.all()
    serializer_class = PhotoGallarySerializers
    lookup_field = 'id'

class VideoGallaryListView(generics.ListAPIView):
    queryset = VideoGallary.objects.all().order_by('-id')
    serializer_class = VideoGallarySerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['videoTitle']

class VideoGallaryDetailView(generics.RetrieveDestroyAPIView):
    queryset = VideoGallary.objects.all()
    serializer_class = VideoGallarySerializers
    lookup_field = 'id'