from rest_framework import serializers
from django_filters import rest_framework as filters
from .models import Account


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'uid',
            'balance'
        ]


class AccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'uid',
            'state',
            'balance',
            'create_at'
        ]


class AccountFilter(filters.FilterSet):
    start_time = filters.DateTimeFilter(field_name="create_at", lookup_expr='gte')
    end_time = filters.DateTimeFilter(field_name="create_at", lookup_expr='lte')

    class Meta:
        model = Account
        fields = ['uid', 'start_time', 'end_time', 'user__email']
