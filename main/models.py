import json

from cart.models import Transaction

from uuid import uuid4

from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    linkID = models.UUIDField(
        primary_key=False, default=uuid4, editable=True, unique=False
    )
    activated = models.BooleanField(default=False)
    resetTime = models.DateTimeField(default=now, editable=True)
    record = models.ManyToManyField(Transaction, default=None)
    phone_regex = RegexValidator(regex=r"^[1-9][0-9]{2}-?[0-9]{3}-?[0-9]{3}$")
    phone_number = models.CharField(validators=[phone_regex], max_length=11, blank=True)
    address = models.CharField(max_length=300, blank=True)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        if self.is_superuser:
            self.activated = True
