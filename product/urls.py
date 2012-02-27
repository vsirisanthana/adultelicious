from django.conf.urls.defaults import patterns, url
from django.views.decorators.cache import cache_page
from serene.views import CreatableInstanceModelView, PaginatedListOrCreateModelView

from product.resources import CategoryResource, ProductResource, PriceResource


urlpatterns = patterns('',
    url(r'^categories/?$', cache_page(15)(PaginatedListOrCreateModelView.as_view(resource=CategoryResource)), name='category_list_or_create'),
    url(r'^categories/(?P<id>\d+)/?$', cache_page(15)(CreatableInstanceModelView.as_view(resource=CategoryResource)), name='category_instance'),
    url(r'^products/?$', cache_page(15)(PaginatedListOrCreateModelView.as_view(resource=ProductResource)), name='product_list_or_create'),
    url(r'^products/(?P<id>\d+)/?$', cache_page(15)(CreatableInstanceModelView.as_view(resource=ProductResource)), name='product_instance'),
)
