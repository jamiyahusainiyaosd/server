from django.urls import path
from .views import AdmissionListCreateView, AdmissionDetailsView

urlpatterns = [
    path('', AdmissionListCreateView.as_view(), name='admission-list-create'),
    path('/<uuid:pk>', AdmissionDetailsView.as_view(), name='admisstin-detail')
]