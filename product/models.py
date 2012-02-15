from django.db import models
from serenesiri.models import Model


CURRENCY_CHOICES = (
    ('EUR', 'Euros'),
    ('GBP', 'Great Britain Pounds'),
    ('THB', 'Thai Baht'),
    ('USD', 'US Dollars'),
)


class Category(Model):
    name = models.CharField(max_length=1024)


class Product(Model):
    name = models.CharField(max_length=1024)
    category = models.ForeignKey(Category)
    description = models.TextField()


class Price(Model):
    product = models.ForeignKey(Product)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    value = models.DecimalField(max_digits=20, decimal_places=8)