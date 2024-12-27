from rest_framework import serializers
from ..models import Payment

class PaymentListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class PaymentRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class PaymentWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'