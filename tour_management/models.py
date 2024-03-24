from django.contrib.auth import get_user_model
from django.contrib.gis.db.models import PointField
from django.db import models
from django.db.models import Q
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from core.mixins.models import BaseModel, CodeFieldMixin, NameFieldMixin
from core.models import Category, City

User = get_user_model()


class PlaceCategory(BaseModel):
    place = models.ForeignKey(
        verbose_name=_("place"), to="Place", on_delete=models.DO_NOTHING, related_name="categories_of_places"
    )
    category = models.ForeignKey(
        verbose_name=_("category"), to=Category, on_delete=models.DO_NOTHING, related_name="categories_of_places"
    )

    class Meta:
        verbose_name = "Place Category"
        verbose_name_plural = "Place Categories"
        db_table = "place_categories"
        constraints = [
            models.UniqueConstraint(
                fields=["place", "category"],
                condition=Q(deleted_at__isnull=True),
                name="place_category_unique_constraint",
            )
        ]

    def __str__(self):
        return f"{self.place.name} - {self.category.name}"


class Place(BaseModel, NameFieldMixin, CodeFieldMixin):
    slug = models.SlugField(verbose_name=_("slug"), unique=True, db_index=True)
    city = models.ForeignKey(verbose_name=_("city"), to=City, on_delete=models.DO_NOTHING, related_name="places")
    address = models.TextField(verbose_name=_("address"), null=True, blank=True)
    description = models.TextField(verbose_name=_("description"), null=True, blank=False)
    visiting_fees = models.DecimalField(verbose_name=_("visiting fees"), max_digits=10, decimal_places=2, default=0.00)
    website = models.URLField(verbose_name=_("website"), blank=True)
    location = PointField()
    place_categories = models.ManyToManyField(
        verbose_name=_("place categories"),
        to=Category,
        through=PlaceCategory,
        related_name="place_categories",
        through_fields=("place", "category"),
    )

    class Meta:
        verbose_name = "Place"
        verbose_name_plural = "Places"
        db_table = "places"
        constraints = [
            models.UniqueConstraint(
                fields=["location"],
                condition=Q(deleted_at__isnull=True),
                name="location_unique_constraint",
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.city.name} --> Location: {self.location}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class PlaceImage(BaseModel):
    place = models.ForeignKey(
        verbose_name=_("place"), to="Place", on_delete=models.DO_NOTHING, related_name="images_of_places"
    )
    image = models.CharField(verbose_name=_("image"), max_length=1000)

    class Meta:
        verbose_name = "Place Image"
        verbose_name_plural = "Place Images"
        db_table = "place_images"

    def __str__(self):
        return f"{self.place.name}"
