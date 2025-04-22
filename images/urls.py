from django.urls import path
from .views import ImageListCreateAPIView, ImageDetailAPIView

urlpatterns = [
    path('', ImageListCreateAPIView.as_view(), name='image-list-create'),  
    path('/<uuid:pk>', ImageDetailAPIView.as_view(), name='image-details'),
]