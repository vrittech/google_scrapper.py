# serializers.py
from rest_framework import serializers

class WebScrapingSerializer(serializers.Serializer):
    data = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )
