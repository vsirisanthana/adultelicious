from django.test import TestCase
from product.models import Category, Product


class TestCategory(TestCase):

    def setUp(self):
        self.vibrators = Category.objects.create(name='Vibrators')

    def test_category(self):
        self.assertEqual(self.vibrators.name, 'Vibrators')
        self.assertEqual(unicode(self.vibrators), 'Vibrators')