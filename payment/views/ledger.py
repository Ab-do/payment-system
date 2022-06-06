from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from payment.serializers.ledger import LedgerSerializer, LedgerFilter
from django_filters.rest_framework import DjangoFilterBackend
from payment.models import Transfer
from rest_framework import permissions
from rest_framework import generics


class LedgerList(generics.ListAPIView):
    model = Transfer
    serializer_class = LedgerSerializer
    filterset_class = LedgerFilter
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Transfer.objects.all()
