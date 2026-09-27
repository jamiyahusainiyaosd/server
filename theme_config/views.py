from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import ThemeSetting, PrayerTime, AdmissionStatus, ContactSetting
from .serializers import ThemeSettingSerializer, PrayerTimeSerializer, AdmissionStatusSerializer, ContactSettingSerializer

class ThemeSettingView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        setting = ThemeSetting.get_solo()
        serializer = ThemeSettingSerializer(setting)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AdmissionStatusView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        obj = AdmissionStatus.get_solo()
        serializer = AdmissionStatusSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PrayerTimeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        prayer = PrayerTime.get_solo()
        serializer = PrayerTimeSerializer(prayer)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ContactSettingView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        contact = ContactSetting.get_solo()
        serializer = ContactSettingSerializer(contact)
        return Response(serializer.data, status=status.HTTP_200_OK)
