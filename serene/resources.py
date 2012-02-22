from django.db import models
from djangorestframework.resources import ModelResource as DrfModelResource
from djangorestframework.serializer import _SkipField
from serene.serializers import RelatedSerializer


class ModelResource(DrfModelResource):
    exclude = ()
    include = ('links',)
    related_serializer = RelatedSerializer
    _links = {}

    def links(self, instance):
        self._links['self'] = {
            'href': self.url(instance),
            'rel': 'self',
            }
        return self._links

    def filter_response(self, obj):
        self._links = {}
        return super(ModelResource, self).filter_response(obj)

    def serialize_val(self, key, obj):
        serialized_val = super(ModelResource, self).serialize_val(key, obj)
        if isinstance(obj, models.Model):
            link = dict(serialized_val)
            link['rel'] = key
            link['href'] = link['links']['href']
            del link['id']
            del link['links']
            self._links[key] = link

#            del serialized_val['href']
            return serialized_val
        else:
            return serialized_val