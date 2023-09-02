from rest_framework import serializers
from .models import PayPalOrder

class PayPalOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayPalOrder
        fields = ('payment_id', 'user', 'cart', 'created_at', 'updated_at', 'approved')