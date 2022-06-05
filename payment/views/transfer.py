from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from payment.serializers.transfer import *


class Transfer(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = {'res': 'test'}
        return Response(data, status=status.HTTP_200_OK)
