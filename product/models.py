import json

from django.db import models


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
            title  = item['title']
            sdesc  = item['sdesc']
            desc   = item['desc']
            price  = item['price']
            amount = item['amount']
            sold   = item['sold']
            rating = item['rating']
            img    = item['img']
            Product(title=title, sdesc=sdesc, desc=desc, price=price, amount=amount, sold=sold, rating=rating, img=img).save()

        return 

    def __str__(self):
        return self.title


