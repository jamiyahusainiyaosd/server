from django.urls import path
from .views import ContactFormView
from theme_config.views import ContactSettingView

urlpatterns = [
    path('', ContactFormView.as_view(), name='contact_forms'),
    path('info/', ContactSettingView.as_view(), name='contact_info'),
]
