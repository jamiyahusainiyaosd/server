from django.urls import path
from .views import (
    LatestNoticesApiView, NoticeDetailsApiView,
    NoticeListApiView)

urlpatterns = [
    path('', NoticeListApiView.as_view(), name='notices-list'),
    path('<int:pk>/', NoticeDetailsApiView.as_view(), name='notices-details'),
    path('latest/', LatestNoticesApiView.as_view(), name='notices-list-recent'),
]