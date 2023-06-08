from rest_framework import serializers
from .models import Makesentence
 
# Serializer for our API
class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Makesentence
        fields=('word','sentence', 'meaning')