import re
from rest_framework import serializers
from .models import FormerStudent

MOBILE_RE = re.compile(r"^\+?\d{10,15}$")  

class FormerStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormerStudent
        fields = [
            "id", "image", "name", "address", "pass_year", "current", "mobile",
            "created_at", "updated_at"
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_mobile(self, value: str) -> str:
        value = value.strip()
        if not MOBILE_RE.match(value):
            raise serializers.ValidationError("Invalid mobile number format.")
        return value

    def validate_pass_year(self, value):
        if value is None:
            return value
        if value < 1900 or value > 2100:
            raise serializers.ValidationError("pass_year must be between 1900 and 2100.")
        return value