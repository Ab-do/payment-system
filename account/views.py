from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BalanceSerializer
from .models import Account
from django.shortcuts import get_object_or_404


class BalanceView(APIView):

    def get(self, request, uid):
        account = get_object_or_404(Account, uid=uid)
        balance_serializer = BalanceSerializer(account)
        return Response(data=balance_serializer.data, status=status.HTTP_200_OK)
