from rest_framework import serializers
from .models import TeacherModel

class TeacherSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(source='image', read_only=True)

    class Meta:
        model = TeacherModel
        fields = ['id', 'name', 'designation', 'phone_number', 'image', 'avatar', 'created_at', 'updated_at']
        extra_kwargs = {
            'name' : {'required' : True},
            'designation' : {'required' : True},
            'phone_number' : {'required' : True},
        }
