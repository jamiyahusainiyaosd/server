from django.urls import path
from .views import (ExpatriateGrantListCreateAPIView, ExpatriateGrantDetailAPIView)
urlpatterns = [
    path("expatriateGrant", ExpatriateGrantListCreateAPIView.as_view(), name="expatriateGrant-list-create"),
    path("expatriateGrant/<uuid:expatriategrant_id>", ExpatriateGrantDetailAPIView.as_view(), name="expatriateGrant-detail"),
]