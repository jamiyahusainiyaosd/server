from django.urls import path
from .views import TeacherListApiView

urlpatterns = [
    path('', TeacherListApiView.as_view(), name='teacher-list'),
]