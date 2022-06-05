from django.contrib.auth.models import User
from django.db import models
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
    balance = models.FloatField(default=0.0)
    create_at = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=10, choices=ACCOUNT_STATE, default='draft')

    def __str__(self):
        return str(self.uid)
