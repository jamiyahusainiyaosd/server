from django.urls import path
from .views import NoticeListApiView, NoticeDetailsApiView

urlpatterns = [
    path('', NoticeListApiView.as_view(), name='all-notices'),
    path('<int:pk>/', NoticeDetailsApiView.as_view(), name='single-notice'),
]