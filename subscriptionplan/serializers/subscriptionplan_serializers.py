from rest_framework import serializers
from ..models import SubscriptionPlan

class SubscriptionPlanListSerializers(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'

class SubscriptionPlanRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'

class SubscriptionPlanWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'