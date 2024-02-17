from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from core.mixins.models import BaseModel, CodeFieldMixin, NameFieldMixin


class Country(BaseModel, NameFieldMixin, CodeFieldMixin):
    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
        db_table = "countries"
        constraints = [
            models.UniqueConstraint(
                fields=["code"], condition=Q(deleted_at__isnull=True), name="country_code_unique_constraint"
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.code}"


class State(BaseModel, NameFieldMixin, CodeFieldMixin):
    country = models.ForeignKey(
        verbose_name=_("country"), to=Country, on_delete=models.DO_NOTHING, related_name="states"
    )

    class Meta:
        verbose_name = _("State")
        verbose_name_plural = _("States")
        db_table = "states"
        constraints = [
            models.UniqueConstraint(
                fields=["code"], condition=Q(deleted_at__isnull=True), name="state_code_unique_constraint"
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.code}"


class City(BaseModel, NameFieldMixin, CodeFieldMixin):
    state = models.ForeignKey(verbose_name=_("state"), to=State, on_delete=models.DO_NOTHING, related_name="cities")

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")
        db_table = "cities"
        constraints = [
            models.UniqueConstraint(
                fields=["code"], condition=Q(deleted_at__isnull=True), name="city_code_unique_constraint"
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.code}"


class Language(BaseModel, NameFieldMixin, CodeFieldMixin):
    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")
        db_table = "languages"
        constraints = [
            models.UniqueConstraint(
                fields=["code"], condition=Q(deleted_at__isnull=True), name="language_code_unique_constraint"
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.code}"


class Category(BaseModel, NameFieldMixin, CodeFieldMixin):
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        db_table = "categories"
        constraints = [
            models.UniqueConstraint(
                fields=["code"], condition=Q(deleted_at__isnull=True), name="category_code_unique_constraint"
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.code}"
