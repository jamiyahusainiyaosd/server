from django.urls import path
from .views import FinanicialReportListView, FinanicialReportDetailView

urlpatterns = [
    path('', FinanicialReportListView.as_view(), name='financial-report-list'),
    path('/<uuid:pk>', FinanicialReportDetailView.as_view(), name='financial-report-detail')
]
