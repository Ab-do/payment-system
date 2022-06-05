from django.db import models
from account.models import Account
import uuid


class Transfer(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='receiver')
    amount = models.FloatField()

    def __str__(self):
        return str(self.uid)

    def save(self, *args, **kwargs):
        if float(self.amount) <= 0.0:
            raise ValueError("you have to put a valid value")
        if self.sender == self.receiver:
            raise ValueError("It is not possible to transfer to the same person.")
        if not self.transfer():
            raise ValueError("error")

        return super(Transfer, self).save(args, kwargs)

    def transfer(self):
        try:
            amount = float(self.amount)
            self.receiver.balance = float(self.receiver.balance) + amount
            self.sender.balance = float(self.sender.balance) - amount
            self.sender.save()
            self.receiver.save()
            return True
        except Exception as error:
            print(error)
            return False
