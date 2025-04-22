from rest_framework import serializers

class ContactFormSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=11)
    email = serializers.EmailField()
    message = serializers.CharField(max_length=1000)