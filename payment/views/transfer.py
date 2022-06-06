from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from payment.serializers.transfer import TransferSerializer
from payment.models import Transfer
from account.models import Account


class TransferDetailsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, uid, *args, **kwargs):
        transfer = get_object_or_404(Transfer, uid=uid)
        transfer_serializer = TransferSerializer(transfer)
        return Response(data=transfer_serializer.data, status=status.HTTP_200_OK)


class TransferView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        transfer = Transfer.objects.all()
        print(request.headers)
        transfer_serializer = TransferSerializer(transfer, many=True)
        return Response(data=transfer_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            amount = float(data['amount'])
            uid_sender = data['uid_sender']
            uid_receiver = data['uid_receiver']
        except KeyError as key:
            return Response(data={'message': f'{key} required.'}, status=status.HTTP_400_BAD_REQUEST)
        sender = get_object_or_404(Account, uid=uid_sender)
        if not float(sender.balance) - amount > 0.0:
            return Response(data={'message': 'Your balance is insufficient.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        receiver = get_object_or_404(Account, uid=uid_receiver)
        data['sender'] = sender.id
        data['receiver'] = receiver.id
        transfer_serializer = TransferSerializer(data=request.data)
        try:
            transfer_serializer.is_valid(raise_exception=True)
            transfer_serializer.save()
            return Response(data=transfer_serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as error:
            return Response(data={'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)
