from rest_framework import serializers
from ..models import ScrapedData

class ScrapedDataListSerializers(serializers.ModelSerializer):
    class Meta:
        model = ScrapedData
        fields = '__all__'

class ScrapedDataRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = ScrapedData
        fields = '__all__'

class ScrapedDataWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = ScrapedData
        fields = '__all__'