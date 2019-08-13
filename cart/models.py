from django.db import models
from django.utils.timezone import now


class TransactionHistory(models.Model):
    totalCost = models.DecimalField(max_digits=1000000, decimal_places=2)
    items = models.TextField(default=None)
    timeHis = models.DateTimeField(default=now, editable=True)
    discount = models.CharField(max_length=200, default='')

    # def __str__(self):
    #     return items
