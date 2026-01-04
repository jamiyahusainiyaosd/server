from django.urls import path
from .views import (FormerStudentDetailAPIView, FormerStudentListCreateAPIView)

urlpatterns = [
    path("/formerStudent", FormerStudentListCreateAPIView.as_view(), name="formerStudent-list-create"),
    path("/formerStudent/<uuid:formerStudent_id>", FormerStudentDetailAPIView.as_view(), name="formerStudent-detail"),
]