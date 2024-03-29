from serene import models


CURRENCY_CHOICES = (
    ('EUR', 'Euros'),
    ('GBP', 'Great Britain Pounds'),
    ('THB', 'Thai Baht'),
    ('USD', 'US Dollars'),
)


class Category(models.Model):
    name = models.CharField(max_length=1024)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('category_instance', (), {'id': self.id})


class Product(models.Model):
    name = models.CharField(max_length=1024)
    category = models.ForeignKey(Category)
    description = models.TextField()

    @models.permalink
    def get_absolute_url(self):
        return ('product_instance', (), {'id': self.id})


class Price(models.Model):
    product = models.ForeignKey(Product)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    value = models.DecimalField(max_digits=20, decimal_places=8)