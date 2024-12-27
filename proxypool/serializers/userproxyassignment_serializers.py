from rest_framework import serializers
from ..models import UserProxyAssignment

class UserProxyAssignmentListSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProxyAssignment
        fields = '__all__'

class UserProxyAssignmentRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProxyAssignment
        fields = '__all__'

class UserProxyAssignmentWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProxyAssignment
        fields = '__all__'