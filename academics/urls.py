from django.urls import path
from .views import AcademicListApiView, AcademicDetailsListApiView

urlpatterns = [
    path('', AcademicListApiView.as_view(), name='academic-list'),
    path('<uuid:pk>/', AcademicDetailsListApiView.as_view(), name='academic-detail'),
]