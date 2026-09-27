from django.urls import path
from .views import (
    AdmissionListCreateView,
    AdmissionDetailsView,
    AdmissionRuleListView,
    AdmissionStatusView,
)

urlpatterns = [
    path('', AdmissionListCreateView.as_view(), name='admission-list-create'),
    path('status/', AdmissionStatusView.as_view(), name='admission-status'),
    path('rules/', AdmissionRuleListView.as_view(), name='admission-rules-list'),
    path('<uuid:pk>', AdmissionDetailsView.as_view(), name='admisstin-detail')
]
