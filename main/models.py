import json

from django.db import models
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class User(AbstractUser):
  linkID    = models.UUIDField(primary_key=False,default=uuid4, editable=True, unique=False)
  activated = models.BooleanField(default=False)
  resetTime = models.DateTimeField(default=now, editable=True)
  buyRecord = models.TextField(blank=True, editable=True)

  def set_buyRecord(self, data):
    self.buyRecord += json.dumps(data)

  def get_buyRecord(self):
    buyRecord = json.loads(self.buyRecord)

    return buyRecord

