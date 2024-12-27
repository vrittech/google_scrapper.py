from rest_framework import serializers
from ..models import WebScrapingTask

class WebScrapingTaskListSerializers(serializers.ModelSerializer):
    class Meta:
        model = WebScrapingTask
        fields = '__all__'

class WebScrapingTaskRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = WebScrapingTask
        fields = '__all__'

class WebScrapingTaskWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = WebScrapingTask
        fields = '__all__'