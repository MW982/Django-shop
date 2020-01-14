from django.db import models
from django.utils.timezone import now


class DiscountCode(models.Model):
    code = models.CharField(default=None, max_length=100)
    percent = models.IntegerField(default=10)

    def __str__(self):
        return self.code


class Transaction(models.Model):
    totalCost = models.DecimalField(max_digits=1000000, decimal_places=2)
    items = models.TextField(default=None)
    timeHis = models.DateTimeField(default=now, editable=True)
