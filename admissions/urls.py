from django.urls import path
from .views import AdmissionListCreateView, AdmissionDetailsView, AdmissionRuleListView

urlpatterns = [
    path('', AdmissionListCreateView.as_view(), name='admission-list-create'),
    path('rules/', AdmissionRuleListView.as_view(), name='admission-rules-list'),
    path('<uuid:pk>', AdmissionDetailsView.as_view(), name='admisstin-detail')
]
