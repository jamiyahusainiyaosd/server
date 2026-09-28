from django.urls import path
from .views import (
    StudentResueltsDetailView, 
    StudentResueltsListCreateView,
    TopAchieverListView,
    TopAchieverDetailView,
)

urlpatterns = [
    path('top-achievers/', TopAchieverListView.as_view(), name='top-achievers-list'),
    path('top-achievers/<uuid:pk>/', TopAchieverDetailView.as_view(), name='top-achievers-detail'),
    path('', StudentResueltsListCreateView.as_view(), name='results-list-create'),
    path('<uuid:pk>/', StudentResueltsDetailView.as_view(), name='results-detail'),
]
