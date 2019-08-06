import json

from django.db import models

# Create your models here.


class Product(models.Model):
    title  = models.CharField(max_length=200)
    sdesc  = models.CharField(max_length=500)
    desc   = models.TextField()
    price  = models.DecimalField(max_digits=10000,decimal_places=2)
    amount = models.PositiveIntegerField(default=0)
    sold   = models.PositiveIntegerField(default=0)
    rating = models.PositiveSmallIntegerField(default=0)
    img    = models.FileField(default='noimage.jpg')

    def read_json(self, path):
        with open(path) as products_file:
            products = json.load(products_file)

        for item in products['Products']:
            title = item['title']
        #    sdesc = item['sdesc']
            price = item['price']
            Product(title=title, price=price).save()
        #    print(item['title'])

        return 

    def __str__(self):
        return self.title


