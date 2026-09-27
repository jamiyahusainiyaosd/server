from django.urls import path
from .views import ThemeSettingView, PrayerTimeView, AdmissionStatusView, ContactSettingView

urlpatterns = [
    path('', ThemeSettingView.as_view(), name='theme-setting'),
    path('admission-status/', AdmissionStatusView.as_view(), name='theme-admission-status'),
    path('prayer-times/', PrayerTimeView.as_view(), name='prayer-times'),
    path('contact/', ContactSettingView.as_view(), name='contact-setting'),
]
