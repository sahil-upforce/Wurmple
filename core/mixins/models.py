import datetime
import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.managers import BaseModelManager


class BaseModel(models.Model):
    public_id = models.UUIDField(verbose_name=_("public id"), default=uuid.uuid4, primary_key=True)
    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("updated at"), auto_now=True)
    deleted_at = models.DateTimeField(verbose_name=_("deleted at"), null=True, blank=True)
    created_by = models.ForeignKey(
        verbose_name=_("created by"),
        to="user_app.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    updated_by = models.ForeignKey(
        verbose_name=_("updated by"),
        to="user_app.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    deleted_by = models.ForeignKey(
        verbose_name=_("deleted by"),
        to="user_app.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    objects = BaseModelManager()
    all_objects = BaseModelManager(alive_only=False)

    class Meta:
        abstract = True

    def delete_related_objects(self):
        related_objects = self._meta.related_objects
        for related_object in related_objects:
            related_manager = getattr(self, related_object.get_accessor_name(), None)
            if related_manager and hasattr(related_manager, "all"):
                for related_obj in related_manager.all():
                    try:
                        related_obj.delete()
                    except ObjectDoesNotExist:
                        continue

    def delete(self, using=None, keep_parents=False):
        self.delete_related_objects()
        self.deleted_at = datetime.datetime.now()
        self.save()

    def hard_delete(self):
        return super().delete()

    @property
    def is_new(self):
        return self._state.adding


class NameFieldMixin(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=225)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(*args, **kwargs)


class CodeFieldMixin(models.Model):
    code = models.CharField(verbose_name=_("code"), max_length=15, db_index=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        super().save(*args, **kwargs)
