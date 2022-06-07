from django.db import models
# from account.models import Account
import uuid

STATE_TRANSFER = [
    ('pending', 'pending'),
    ('error', 'error'),
    ('done', 'done')
]


class Transfer(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    sender = models.ForeignKey('account.Account', on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey('account.Account', on_delete=models.CASCADE, related_name='receiver')
    amount = models.FloatField()
    state = models.CharField(max_length=10, choices=STATE_TRANSFER, default='pending')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.uid)

    def save(self, *args, **kwargs):
        if float(self.amount) <= 0.0:
            raise ValueError("you have to put a valid value")
        if self.sender == self.receiver:
            raise ValueError("It is not possible to transfer to the same person.")
        self.state = 'done'
        return super(Transfer, self).save(*args, **kwargs)
