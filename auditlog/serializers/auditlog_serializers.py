from rest_framework import serializers
from ..models import AuditLog

class AuditLogListSerializers(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'

class AuditLogRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'

class AuditLogWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'