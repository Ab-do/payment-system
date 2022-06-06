from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BalanceSerializer, AccountListSerializer, AccountFilter
from .models import Account
from django.shortcuts import get_object_or_404
from rest_framework import generics


class BalanceView(APIView):

    def get(self, request, uid):
        account = get_object_or_404(Account, uid=uid)
        balance_serializer = BalanceSerializer(account)
        return Response(data=balance_serializer.data, status=status.HTTP_200_OK)


class AccountsList(generics.ListAPIView):
    model = Account
    serializer_class = AccountListSerializer
    filterset_class = AccountFilter

    def get_queryset(self):
        return Account.objects.all()
