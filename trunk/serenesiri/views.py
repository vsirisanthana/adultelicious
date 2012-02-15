from djangorestframework.mixins import InstanceMixin, DeleteModelMixin, ListModelMixin, PaginatorMixin
from djangorestframework.views import ModelView
from serenesiri.mixins import CreateModelMixin, ReadModelMixin, UpdateModelMixin, UpdateOrCreateModelMixin


class InstanceModelView(InstanceMixin, ReadModelMixin, UpdateModelMixin, DeleteModelMixin, ModelView):
    pass


class CreatableInstanceModelView(InstanceMixin, ReadModelMixin, UpdateOrCreateModelMixin, DeleteModelMixin, ModelView):
    pass


class ListOrCreateModelView(ListModelMixin, CreateModelMixin, PaginatorMixin, ModelView):
    limit = 5

    def filter_response(self, obj):
        return super(ListOrCreateModelView, self).filter_response(obj)