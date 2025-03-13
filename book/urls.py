from django.urls import path
from .views import BookIntroductionListView

urlpatterns = [
    path('', BookIntroductionListView.as_view(), name='book-list'),
]