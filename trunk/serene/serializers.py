from django.db import models
from djangorestframework.serializer import Serializer


class RelatedSerializer(Serializer):

    def serialize_model(self, instance):
        """
        serialize_model serializes both Model and dict.
        """
        if isinstance(instance, models.Model):
            return {
                'id': instance.id,
                'title': unicode(instance),
                'links':{
                    'href': instance.get_absolute_url(),
                    'rel': 'self'
                },
                'url': instance.get_absolute_url(),
            }
        else:
            return super(RelatedSerializer, self).serialize_model(instance)