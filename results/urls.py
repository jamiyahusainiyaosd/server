from django.urls import path
from .views import StudentResueltsDetailView, StudentResueltsListCreateView

urlpatterns = [
    path('', StudentResueltsListCreateView.as_view(), name='results-list-create'),
    path('/<uuid:pk>', StudentResueltsDetailView.as_view(), name='results-detail'),
]