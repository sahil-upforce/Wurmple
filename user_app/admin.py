from django.contrib import admin
from django.contrib.auth import get_user_model

from core.admin import BaseAdmin
from user_app.models import Gender, GuideReview, SpokenLanguage, TourCategory

User = get_user_model()


@admin.register(Gender)
class GenderAdmin(BaseAdmin):
    pass


@admin.register(SpokenLanguage)
class SpokenLanguageAdmin(BaseAdmin):
    pass


@admin.register(TourCategory)
class TourCategoryAdmin(BaseAdmin):
    pass


@admin.register(GuideReview)
class GuideReviewAdmin(BaseAdmin):
    pass


@admin.register(User)
class UserAdmin(BaseAdmin):
    pass
