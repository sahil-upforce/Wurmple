from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phone_field import PhoneField

from core.mixins.models import BaseModel, CodeFieldMixin, NameFieldMixin
from core.models import Category, Language


class Gender(BaseModel, NameFieldMixin, CodeFieldMixin):
    class Meta:
        verbose_name = "gender"
        verbose_name_plural = "genders"
        db_table = "genders"

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.name = self.name.strip().title()
        super(Gender, self).save(
            force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields
        )


class SpokenLanguage(BaseModel):
    user = models.ForeignKey(verbose_name=_("user"), to="User", on_delete=models.DO_NOTHING, related_name="languages")
    language = models.ForeignKey(
        verbose_name=_("language"), to=Language, on_delete=models.DO_NOTHING, related_name="languages"
    )
    fluency = models.PositiveSmallIntegerField(verbose_name=_("fluency"), default=1)

    class Meta:
        verbose_name = "Spoken Language"
        verbose_name_plural = "Spoken Languages"
        db_table = "spoken_languages"

    def __str__(self):
        return f"{self.user.username} - {self.language.code} - {self.fluency}"


class TourCategory(BaseModel):
    user = models.ForeignKey(verbose_name=_("user"), to="User", on_delete=models.DO_NOTHING, related_name="categories")
    category = models.ForeignKey(
        verbose_name=_("category"), to=Category, on_delete=models.DO_NOTHING, related_name="categories"
    )

    class Meta:
        verbose_name = "TourCategory"
        verbose_name_plural = "Tour Categories"
        db_table = "tour_categories"

    def __str__(self):
        return f"{self.user.username} - {self.category.name}"


class User(AbstractUser, BaseModel):
    date_joined = None
    email = models.EmailField(verbose_name=_("email address"), unique=True)
    gender = models.ForeignKey(
        verbose_name=_("gender"), to=Gender, on_delete=models.DO_NOTHING, related_name="+", null=True
    )
    phone = PhoneField(verbose_name=_("phone"), blank=True, null=True)
    spoken_languages = models.ManyToManyField(
        verbose_name=_("spoken languages"),
        to=Language,
        through=SpokenLanguage,
        related_name="spoken_languages",
        through_fields=("user", "language"),
    )
    tour_categories = models.ManyToManyField(
        verbose_name=_("tour categories"),
        to=Category,
        through=TourCategory,
        related_name="tour_categories",
        through_fields=("user", "category"),
    )
    # current_location = PointField(verbose_name=_("current location"), null=True, blank=True)
    address = models.TextField(verbose_name=_("address"), blank=True, null=True)
    bio = models.TextField(verbose_name=_("bio"), blank=True, null=True)
    birth_date = models.DateField(verbose_name=_("birth date"), null=True, blank=True)
    profile_picture = models.CharField(verbose_name=_("profile picture"), blank=True, null=True, max_length=1000)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "users"

    def __str__(self):
        return f"{self.username}"


class Tourist(BaseModel):
    user = models.OneToOneField(verbose_name=_("user"), to=User, on_delete=models.DO_NOTHING, related_name="tourist")

    class Meta:
        verbose_name = "Tourist"
        verbose_name_plural = "Tourists"
        db_table = "tourist"

    def __str__(self):
        return f"{self.user.username}"


class GuideReview(BaseModel):
    guide = models.ForeignKey(
        verbose_name=_("guide"), to="Guide", on_delete=models.DO_NOTHING, related_name="guide_reviews"
    )
    tourist = models.ForeignKey(
        verbose_name=_("tourist"), to="Tourist", on_delete=models.DO_NOTHING, related_name="guide_reviews"
    )
    context = models.TextField(verbose_name=_("review context"))
    rating = models.PositiveSmallIntegerField(verbose_name=_("rating"), default=1)

    class Meta:
        verbose_name = "Guide Review"
        verbose_name_plural = "Guide Reviews"
        db_table = "guid_reviews"

    def __str__(self):
        return f"{self.guide.user.username} - {self.context} - {self.rating}"


class Guide(BaseModel):
    user = models.OneToOneField(verbose_name=_("user"), to=User, on_delete=models.DO_NOTHING, related_name="guide")
    is_available = models.BooleanField(verbose_name=_("is available"), default=True)
    experience = models.PositiveSmallIntegerField(verbose_name=_("experience"), default=0)

    class Meta:
        verbose_name = "Guide"
        verbose_name_plural = "Guide"
        db_table = "guids"

    def __str__(self):
        return f"{self.user.username}"
