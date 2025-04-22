from django.urls import path
from .views import BookIntroductionListView, BookIntroductionDetailView

urlpatterns = [
    path('', BookIntroductionListView.as_view(), name='book-list'),
    path('/<uuid:pk>', BookIntroductionDetailView.as_view(), name='book-details'),
]