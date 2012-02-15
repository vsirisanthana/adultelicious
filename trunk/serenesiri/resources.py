from djangorestframework.resources import ModelResource as DrfModelResource


class ModelResource(DrfModelResource):
    exclude = ()
    include = ('links',)

    def links(self, instance):
        return [{
            'href': self.url(instance),
            'rel': 'self',
        }]