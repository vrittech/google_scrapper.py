from rest_framework import serializers
from ..models import APILog

class APILogListSerializers(serializers.ModelSerializer):
    class Meta:
        model = APILog
        fields = '__all__'

class APILogRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = APILog
        fields = '__all__'

class APILogWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = APILog
        fields = '__all__'