from djangorestframework import status
from djangorestframework.mixins import ModelMixin as DrfModelMixin, ReadModelMixin as DrfReadModelMixin, CreateModelMixin as DrfCreateModelMixin
from djangorestframework.response import ErrorResponse, Response


class ReadModelMixin(DrfReadModelMixin):

    def get(self, request, *args, **kwargs):
        instance = super(ReadModelMixin, self).get(request, *args, **kwargs)
        return Response(content=instance, headers={'Last-Modified':instance.last_modified})


class UpdateModelMixin(DrfModelMixin):
    """
    Behavior to update a `model` instance on PUT requests
    """
    def put(self, request, *args, **kwargs):
        model = self.resource.model
        try:
            self.model_instance = self.get_object(*args, **kwargs)

            for (key, val) in self.CONTENT.items():
                setattr(self.model_instance, key, val)
        except model.DoesNotExist:
            raise ErrorResponse(status.HTTP_404_NOT_FOUND)
        self.model_instance.save()
        return self.model_instance


class UpdateOrCreateModelMixin(DrfModelMixin):

    def put(self, request, *args, **kwargs):
        model = self.resource.model
        try:
            self.model_instance = self.get_object(*args, **kwargs)

            for (key, val) in self.CONTENT.items():
                setattr(self.model_instance, key, val)
        except model.DoesNotExist:
            self.model_instance = model(**self.get_instance_data(model, self.CONTENT, *args, **kwargs))
            self.model_instance.save()
            return Response(status.HTTP_201_CREATED, self.model_instance)
        self.model_instance.save()
        return self.model_instance


class CreateModelMixin(DrfCreateModelMixin):

    def post(self, request, *args, **kwargs):
        response = super(CreateModelMixin, self).post(request, *args, **kwargs)
        response.headers.update({
            'Content-Location': self.resource(self).url(response.raw_content)
        })
        return response