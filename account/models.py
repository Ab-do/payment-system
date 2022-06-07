from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from payment.models import Transfer
import uuid

# Create your models here.

ACCOUNT_STATE = [
    ('draft', 'draft'),
    ('active', 'active'),
    ('blocked', 'blocked'),
]


class Account(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=10, choices=ACCOUNT_STATE, default='draft')

    def __str__(self):
        return str(self.uid)

    def balance(self):
        transfers = Transfer.objects.filter(state='done')
        sent = transfers.filter(sender=self).aggregate(Sum('amount'))['amount__sum']
        receiver = transfers.filter(receiver=self).aggregate(Sum('amount'))['amount__sum']
        if sent is None:
            sent = 0.0
        if receiver is None:
            receiver = 0.0
        total = float(receiver) - float(sent)
        return total
