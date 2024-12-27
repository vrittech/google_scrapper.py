from rest_framework import serializers
from ..models import ProxyPool

class ProxyPoolListSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProxyPool
        fields = '__all__'

class ProxyPoolRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProxyPool
        fields = '__all__'

class ProxyPoolWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProxyPool
        fields = '__all__'