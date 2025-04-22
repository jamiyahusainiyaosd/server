from rest_framework import generics, filters
from .models import StudentResults, StudentResultImage
from .serializers import StudentResueltsListSerializer, StudentResueltsDetailSerializer, StudentResultImageSerializer 
from rest_framework.response import Response
from rest_framework import status

class StudentResueltsListCreateView(generics.ListCreateAPIView):
    queryset = StudentResults.objects.all().order_by('-resultCreatedAt') 
    serializer_class = StudentResueltsListSerializer
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
            return Response({"error": "Student result ID and image URLs are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student_result = StudentResults.objects.get(id=student_result_id)
        except StudentResults.DoesNotExist:
            return Response({"error": "Invalid student result ID"}, status=status.HTTP_404_NOT_FOUND)

        uploaded_images = []
        for img_url in image_urls:
            new_image = StudentResultImage.objects.create(student_result=student_result, resultsSheetImg=img_url)
            uploaded_images.append(StudentResultImageSerializer(new_image).data)

        return Response({"message": "Images uploaded successfully", "images": uploaded_images}, status=status.HTTP_201_CREATED)