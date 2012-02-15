from django.db import models


class Model(models.Model):
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
