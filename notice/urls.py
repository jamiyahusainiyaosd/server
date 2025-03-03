from django.urls import path
from .views import NoticeListApiView, NoticeDetailsApiView

urlpatterns = [
    path('<str:notice_type>/', NoticeListApiView.as_view(), name='notices-list'),
    path('<str:notice_type>/<int:pk>/', NoticeDetailsApiView.as_view(), name='notices-detail'),
]