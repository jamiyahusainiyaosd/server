import re
from rest_framework import serializers
from .models import ExpatriateGrant

MOBILE_RE = re.compile(r"^\+?\d{10,15}$") 

class ExpatriateGrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpatriateGrant
        fields = [
            "id", "image", "name", "address", "mobile",
            "member_type", "chadar_amount", "status",
            "created_at", "updated_at"
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_mobile(self, value: str) -> str:
        value = value.strip()
        if not MOBILE_RE.match(value):
            raise serializers.ValidationError("Invalid mobile number format.")
        return value

    def validate_chadar_amount(self, value):
        if value is None:
            return value
        if value < 0:
            raise serializers.ValidationError("chadar_amount cannot be negative.")
        return value