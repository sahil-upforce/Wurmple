from django.contrib import admin

from core.admin import BaseAdmin
from tour_management.models import Place, PlaceCategory, PlaceImage


@admin.register(PlaceCategory)
class PlaceCategoryAdmin(BaseAdmin):
    pass


@admin.register(PlaceImage)
class PlaceImageAdmin(BaseAdmin):
    pass


@admin.register(Place)
class PlaceAdmin(BaseAdmin):
    pass
