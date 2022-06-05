from rest_framework import serializers
from .models import Account


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'uid',
            'balance'
        ]
