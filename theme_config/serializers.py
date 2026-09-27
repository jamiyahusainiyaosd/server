from rest_framework import serializers
from .models import ThemeSetting

class ThemeSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThemeSetting
        fields = ("bg_alt_color", "saved_custom_colors", "updated_at")
