from rest_framework.fields import SerializerMethodField
from rest_framework import serializers
from payment.models import Transfer


class TransferSerializer(serializers.ModelSerializer):
    uid_sender = serializers.CharField(source="sender.uid", read_only=True)
    uid_receiver = serializers.CharField(source="receiver.uid", read_only=True)

    class Meta:
        model = Transfer
        fields = [
            'uid',
            'uid_receiver',
            'amount',
            'uid_sender',
            'sender',
            'receiver'
        ]
