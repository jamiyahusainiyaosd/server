from django.shortcuts import render
from rest_framework import generics
from .serializers import BookIntroductionSerializers
from .models import BookIntroduction
from rest_framework.filters import SearchFilter

class BookIntroductionListView(generics.ListAPIView):
    queryset = BookIntroduction.objects.all().order_by('-bookCreatedAt')
    serializer_class = BookIntroductionSerializers
    filter_backends = [SearchFilter]
    search_fields = ['bookTitle', 'authorName']