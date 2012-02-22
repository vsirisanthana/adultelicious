from django.db.models import *


class Model(Model):
    last_modified = DateTimeField(auto_now=True)

    class Meta:
        abstract = True
