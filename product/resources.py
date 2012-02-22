from serene.resources import ModelResource
from product.models import Category, Product, Price


class CategoryResource(ModelResource):
    model = Category


class ProductResource(ModelResource):
    model = Product


class PriceResource(ModelResource):
    model = Price