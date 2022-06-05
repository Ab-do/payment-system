from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from payment.serializers.ledger import LedgerSerializer, LedgerFilter
from django_filters.rest_framework import DjangoFilterBackend
from payment.models import Transfer
from account.models import Account
from rest_framework import generics
from django_filters import rest_framework as filters


class LedgerList(generics.ListAPIView):
    model = Transfer
    serializer_class = LedgerSerializer
    filterset_class = LedgerFilter

    def get_queryset(self):
        return Transfer.objects.all()
