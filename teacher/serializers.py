from rest_framework import serializers
from .models import TeacherModel

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherModel
        fields = ['id', 'name', 'designation', 'phone_number', 'created_at', 'updated_at']
        extra_kwargs = {
            'name' : {'required' : True},
            'designation' : {'required' : True},
            'phone_number' : {'required' : True},
        }