import json

from cart.models import TransactionHistory

from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class User(AbstractUser):
  linkID    = models.UUIDField(primary_key=False,default=uuid4, editable=True, unique=False)
  activated = models.BooleanField(default=False)
  resetTime = models.DateTimeField(default=now, editable=True)
  record = models.ManyToManyField(TransactionHistory)


