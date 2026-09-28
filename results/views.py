from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from .models import StudentResults, StudentResultImage, TopAchiever
from .serializers import (
    StudentResueltsListSerializer, 
    StudentResueltsDetailSerializer, 
    StudentResultImageSerializer,
    TopAchieverSerializer,
)

class CustomPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 100

class TopAchieverPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

class StudentResueltsListCreateView(generics.ListCreateAPIView):
    queryset = StudentResults.objects.all().order_by('-resultCreatedAt') 
    serializer_class = StudentResueltsListSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['studentClassName']
    ordering_fields = ['resultCreatedAt', 'resultUpdatedAt']  


class StudentResueltsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentResults.objects.all()
    serializer_class = StudentResueltsDetailSerializer


class UploadResultImageView(generics.CreateAPIView):
    serializer_class = StudentResultImageSerializer

    def post(self, request, *args, **kwargs):
        student_result_id = request.data.get('student_result')
        image_urls = request.data.getlist('resultsSheetImg')  

        if not student_result_id or not image_urls:
            return Response({'error': 'Student result ID and image URLs are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student_result = StudentResults.objects.get(id=student_result_id)
        except StudentResults.DoesNotExist:
            return Response({'error': 'Invalid student result ID'}, status=status.HTTP_404_NOT_FOUND)

        uploaded_images = []
        for img_url in image_urls:
            new_image = StudentResultImage.objects.create(student_result=student_result, resultsSheetImg=img_url)
            uploaded_images.append(StudentResultImageSerializer(new_image).data)

        return Response({'message': 'Images uploaded successfully', 'images': uploaded_images}, status=status.HTTP_201_CREATED)


class TopAchieverListView(generics.ListCreateAPIView):
    serializer_class = TopAchieverSerializer
    pagination_class = TopAchieverPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'class_name', 'achievement_title', 'board_name', 'address', 'roll_number']
    ordering_fields = ['order', 'created_at']

    def get_queryset(self):
        queryset = TopAchiever.objects.all().order_by('order', '-created_at')
        category = self.request.query_params.get('category')
        if category and category != 'all':
            queryset = queryset.filter(category=category)
        
        is_featured = self.request.query_params.get('is_featured')
        if is_featured is not None:
            if is_featured.lower() in ['true', '1']:
                queryset = queryset.filter(is_featured=True)
            elif is_featured.lower() in ['false', '0']:
                queryset = queryset.filter(is_featured=False)
                
        academic_year = self.request.query_params.get('academic_year')
        if academic_year:
            queryset = queryset.filter(academic_year=academic_year)
            
        all_param = self.request.query_params.get('all')
        if all_param and all_param.lower() in ['true', '1']:
            self.pagination_class = None
            
        return queryset


class TopAchieverDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TopAchiever.objects.all()
    serializer_class = TopAchieverSerializer
