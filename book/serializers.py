from rest_framework import serializers
from .models import BookIntroduction

class BookIntroductionSerializers(serializers.ModelSerializer):
    class Meta:
        model = BookIntroduction
        fields =  ['id', 'bookTitle', 'bookDescription', 'authorName', 'bookKobarImg', 'bookCreatedAt', 'bookUpdatedAt']