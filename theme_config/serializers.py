from rest_framework import serializers
from .models import ThemeSetting, PrayerTime, AdmissionStatus, ContactSetting

class ThemeSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThemeSetting
        fields = ("bg_alt_color", "saved_custom_colors", "updated_at")

class AdmissionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdmissionStatus
        fields = "__all__"

class PrayerTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrayerTime
        fields = "__all__"

class ContactSettingSerializer(serializers.ModelSerializer):
    bkash_type_display = serializers.CharField(source='get_bkash_type_display', read_only=True)
    nagad_type_display = serializers.CharField(source='get_nagad_type_display', read_only=True)
    rocket_type_display = serializers.CharField(source='get_rocket_type_display', read_only=True)

    class Meta:
        model = ContactSetting
        fields = "__all__"
