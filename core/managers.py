from django.db import models


class BaseModelManager(models.Manager):
    def __init__(self, *args, alive_only=True, **kwargs):
        self.alive_only = alive_only
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return super(BaseModelManager, self).get_queryset().filter(deleted_at__isnull=True)
        return super(BaseModelManager, self).get_queryset()
