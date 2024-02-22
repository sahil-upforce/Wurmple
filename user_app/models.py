from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from phone_field import PhoneField

from core.managers import BaseModelManager
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
        constraints = [
            models.UniqueConstraint(
                fields=["user", "language"],
                condition=Q(deleted_at__isnull=True),
                name="user_language_unique_constraint",
            )
        ]

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
        constraints = [
            models.UniqueConstraint(
                fields=["user", "category"],
                condition=Q(deleted_at__isnull=True),
                name="user_category_unique_constraint",
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.category.name}"


class User(AbstractUser, BaseModel):
    USER_TYPE_TOURIST = "TOURIST"
    USER_TYPE_GUIDE = "GUIDE"
    USER_TYPE_TOURIST_NAME = "Tourist"
    USER_TYPE_GUIDE_NAME = "Guide"
    USER_TYPE_CHOICES = ((USER_TYPE_TOURIST, _(USER_TYPE_TOURIST_NAME)), (USER_TYPE_GUIDE, _(USER_TYPE_GUIDE_NAME)))

    username_validator = UnicodeUsernameValidator()

    date_joined = None
    email = models.EmailField(verbose_name=_("email address"))
    gender = models.ForeignKey(
        verbose_name=_("gender"), to=Gender, on_delete=models.DO_NOTHING, related_name="+", null=True, blank=False
    )
    phone = PhoneField(verbose_name=_("phone"), blank=True, null=True)
    user_type = models.CharField(
        verbose_name=_("user type"), max_length=10, choices=USER_TYPE_CHOICES, default=USER_TYPE_TOURIST, blank=False
    )
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
    birth_date = models.DateField(verbose_name=_("birth date"), null=True, blank=False)
    profile_picture = models.CharField(verbose_name=_("profile picture"), blank=True, null=True, max_length=1000)
    is_available = models.BooleanField(verbose_name=_("is available"), default=True)
    experience = models.PositiveSmallIntegerField(verbose_name=_("experience"), default=0, blank=False)

    objects = BaseModelManager()
    all_objects = BaseModelManager(alive_only=False)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "users"
        constraints = [
            models.UniqueConstraint(
                fields=["username"], condition=Q(deleted_at__isnull=True), name="username_unique_constraint"
            ),
            models.UniqueConstraint(
                fields=["email"], condition=Q(deleted_at__isnull=True), name="email_unique_constraint"
            ),
        ]

    def __str__(self):
        return f"{self.username}"

    def make_inactive_user(self):
        self.active = False
        self.delete()


class GuideReview(BaseModel):
    guide = models.ForeignKey(verbose_name=_("guide"), to=User, on_delete=models.DO_NOTHING, related_name="reviews")
    tourist = models.ForeignKey(
        verbose_name=_("tourist"), to=User, on_delete=models.DO_NOTHING, related_name="guide_reviews"
    )
    context = models.TextField(verbose_name=_("review context"))
    rating = models.PositiveSmallIntegerField(verbose_name=_("rating"), default=1)

    class Meta:
        verbose_name = "Guide Review"
        verbose_name_plural = "Guide Reviews"
        db_table = "guid_reviews"

    def __str__(self):
        return f"{self.guide.username} - {self.context} - {self.rating}"
