from django.test import TestCase

# from django.core.urlresolvers import reverse

from .models import Product


class ProductTestCase(TestCase):
    def helper_Product(self, title="test", price=999):
        return Product.objects.create(title=title, price=price)

    def test_Product(self):
        p = self.helper_Product()
        self.assertEqual(p.__str__(), p.title)


class ViewsTestCase(TestCase):
    def setUp(self):
        return

    def test_login(self):
        pass
