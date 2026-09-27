from django.urls import path
from .views import ThemeSettingView

urlpatterns = [
    path('', ThemeSettingView.as_view(), name='theme-setting'),
]
