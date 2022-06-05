from rest_framework.fields import SerializerMethodField
from rest_framework import serializers
from payment.models import Transfer
from django_filters import rest_framework as filters


class LedgerFilter(filters.FilterSet):
    start_time = filters.DateTimeFilter(field_name="create_at", lookup_expr='gte')
    end_time = filters.DateTimeFilter(field_name="create_at", lookup_expr='lte')

    class Meta:
        model = Transfer
        fields = ['start_time', 'end_time']


class LedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'
