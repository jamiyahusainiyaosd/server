from django.urls import path
from .views import (
    LatestNoticesApiView, NoticeDetailsApiView,
    NoticeListApiView, AnnouncementListApiView)

urlpatterns = [
    path('', NoticeListApiView.as_view(), name='notices-list'),
    path('latest', LatestNoticesApiView.as_view(), name='notices-list-recent'),
    path('announcements', AnnouncementListApiView.as_view(), name='announcements-list'),
    path('<uuid:pk>', NoticeDetailsApiView.as_view(), name='notices-details'),
]
