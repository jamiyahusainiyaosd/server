from django.urls import path
from .views import (
    PhotoGallaryListView, PhotoGallaryDetailView,
    VideoGallaryListView, VideoGallaryDetailView
)

urlpatterns = [
    path('/photo', PhotoGallaryListView.as_view(), name='photo-gallery'),
    path('/photo/<uuid:id>', PhotoGallaryDetailView.as_view(), name='photo-gallery-detail'),
    path('/video', VideoGallaryListView.as_view(), name='video-gallery'),
    path('/video/<uuid:id>', VideoGallaryDetailView.as_view(), name='video-gallery-detail'),
]